import fitz
import torch
from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification
from PIL import Image
import numpy as np
from typing import List, Dict
import re

class PDFProcessor:
    def __init__(self):
        # Initialize LayoutLMv2 for token classification (table extraction)
        self.processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")
        self.model = LayoutLMv2ForTokenClassification.from_pretrained("microsoft/layoutlmv2-base-uncased")
        
    def extract_table_data(self, texts: List[str], boxes: List[List[int]], predictions: List[int]) -> List[Dict]:
        """Extract structured table data from the detected text and boxes"""
        table_data = []
        current_row = []
        last_y = None
        
        # Sort text blocks by y-coordinate (top to bottom) and x-coordinate (left to right)
        sorted_items = sorted(zip(texts, boxes), key=lambda x: (x[1][1], x[1][0]))
        
        for text, box in sorted_items:
            current_y = box[1]
            
            # Check if this is a new row based on y-coordinate
            if last_y is not None and abs(current_y - last_y) > 20:  # Threshold for new row
                if current_row:
                    table_data.append(current_row)
                    current_row = []
            
            # Clean and process the text
            cleaned_text = text.strip()
            if self.is_table_content(cleaned_text):
                current_row.append({
                    'text': cleaned_text,
                    'bbox': box,
                })
            
            last_y = current_y
        
        # Add the last row if it exists
        if current_row:
            table_data.append(current_row)
        
        return self.structure_table_data(table_data)
    
    def is_table_content(self, text: str) -> bool:
        """Check if the text is likely to be part of a table"""
        # Common patterns in invoice tables
        patterns = [
            r'\d+',  # Numbers
            r'\$?\d+\.?\d*',  # Currency amounts
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # Dates
            r'qty|quantity|description|amount|total|price|item|unit|subtotal',  # Common table headers
        ]
        
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def structure_table_data(self, raw_table_data: List[List[Dict]]) -> List[Dict]:
        """Convert raw table data into structured format"""
        if not raw_table_data:
            return []
        
        # Try to identify headers from the first row
        headers = []
        if raw_table_data[0]:
            headers = [item['text'].lower() for item in raw_table_data[0]]
        
        structured_data = []
        for row in raw_table_data[1:]:  # Skip header row
            row_data = {}
            for idx, cell in enumerate(row):
                header = headers[idx] if idx < len(headers) else f'column_{idx}'
                row_data[header] = cell['text']
            structured_data.append(row_data)
        
        return structured_data

    async def process_pdf(self, content: bytes) -> dict:
        # Convert PDF bytes to document
        pdf_document = fitz.open(stream=content, filetype="pdf")
        results = []
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # Convert page to image
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Get text and bounding boxes
            text_blocks = page.get_text("blocks")
            texts = []
            boxes = []
            
            for block in text_blocks:
                x0, y0, x1, y1, text, *_ = block
                texts.append(text)
                # Normalize coordinates
                boxes.append([
                    int(x0), int(y0), int(x1), int(y1)
                ])
            
            # Prepare inputs for LayoutLM
            encoding = self.processor(
                img,
                text=texts,
                boxes=boxes,
                return_tensors="pt",
                padding="max_length",
                truncation=True
            )
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**encoding)
                predictions = outputs.logits.argmax(-1).squeeze().tolist()
            
            # Extract table data
            table_data = self.extract_table_data(texts, boxes, predictions)
            
            results.append({
                "page": page_num + 1,
                "table_data": table_data,
                "raw_texts": texts,
                "boxes": boxes
            })
            
        return results 