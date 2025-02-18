from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf_processor import PDFProcessor

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_processor = PDFProcessor()

@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    content = await file.read()
    result = await pdf_processor.process_pdf(content)
    return {"result": result} 