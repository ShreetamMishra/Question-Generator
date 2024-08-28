import React from 'react';

function GeneratedQA({ data }) {
  return (
    <div className="card mt-4 border-light shadow-sm">
      <div className="card-header">
        <h5>Generated Q&A</h5>
      </div>
      <div className="table-responsive">
        <table className="table table-flush">
          <thead>
            <tr>
              <th>Question</th>
              <th>Answer</th>
            </tr>
          </thead>
          <tbody>
            {data.map((qa, index) => (
              <tr key={index}>
                <td>{qa[0]}</td>
                <td>{qa[1]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default GeneratedQA;
