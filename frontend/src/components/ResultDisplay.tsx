import React from 'react';

interface TableData {
  [key: string]: string;
}

interface ProcessedResult {
  page: number;
  table_data: TableData[];
  raw_texts: string[];
  boxes: number[][];
}

interface Props {
  results: ProcessedResult[];
}

export const ResultDisplay: React.FC<Props> = ({ results }) => {
  return (
    <div className="space-y-6">
      {results.map((result, pageIndex) => (
        <div key={pageIndex} className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Page {result.page}</h2>
          
          {result.table_data.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    {Object.keys(result.table_data[0]).map((header, idx) => (
                      <th
                        key={idx}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {result.table_data.map((row, rowIdx) => (
                    <tr key={rowIdx}>
                      {Object.values(row).map((cell, cellIdx) => (
                        <td
                          key={cellIdx}
                          className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                        >
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500">No table data found on this page</p>
          )}
        </div>
      ))}
    </div>
  );
}; 