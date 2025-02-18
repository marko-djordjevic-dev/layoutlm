import React, { useState } from 'react';
import axios from 'axios';
import { ProcessingStatus } from './ProcessingStatus';
import { ResultDisplay } from './ResultDisplay';
import { UploadError } from './UploadError';

interface ProcessedResult {
  page: number;
  texts: string[];
  boxes: number[][];
  prediction: number;
}

export const PDFUploader: React.FC = () => {
  const [results, setResults] = useState<ProcessedResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.type.includes('pdf')) {
      setError('Please upload a PDF file');
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/process-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data.result);
    } catch (error) {
      setError('Error processing PDF. Please try again.');
      console.error('Error processing PDF:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow p-6">
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload PDF Document
        </label>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100
            cursor-pointer"
        />
      </div>

      {loading && <ProcessingStatus />}
      {error && <UploadError message={error} />}
      {results.length > 0 && <ResultDisplay results={results} />}
    </div>
  );
}; 