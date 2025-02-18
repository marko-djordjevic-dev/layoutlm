import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold text-gray-900">PDF Document Parser</h1>
        <p className="text-gray-600 mt-1">Upload and analyze PDF documents using LayoutLM</p>
      </div>
    </header>
  );
}; 