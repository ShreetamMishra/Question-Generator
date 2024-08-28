import React from 'react';
import { useLocation } from 'react-router-dom';
import GeneratedQA from './GeneratedQA';

function GeneratedPage() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const data = queryParams.get('data');
  const generatedQA = data ? JSON.parse(decodeURIComponent(data)) : [];

  return (
    <div className="container mt-4">
      {generatedQA.length > 0 ? (
        <GeneratedQA data={generatedQA} />
      ) : (
        <p>No results to display</p>
      )}
    </div>
  );
}

export default GeneratedPage;
