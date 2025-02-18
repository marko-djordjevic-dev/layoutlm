import React from 'react';
import { PDFUploader } from './components/PDFUploader';
import { Header } from './components/Header';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto py-8">
        <PDFUploader />
      </main>
    </div>
  );
};

export default App; 