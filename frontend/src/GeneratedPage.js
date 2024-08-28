import React from 'react';
import { useLocation } from 'react-router-dom';
import DataTable from 'react-data-table-component';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import printJS from 'print-js';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';  
import './App.css';
import GeneratedQA from './GeneratedQA';

pdfMake.vfs = pdfFonts.pdfMake.vfs; 

function GeneratedPage() {
  const location = useLocation();
  const generatedQA = location.state?.data || [];

  const columns = [
    {
      name: 'Question',
      selector: row => row[0],
      sortable: true,
    },
    {
      name: 'Answer',
      selector: row => row[1],
      sortable: true,
    },
  ];

  const handlePrint = () => {

    const printContent = `
      <html>
      <head>
        <style>
          table { width: 100%; border-collapse: collapse; }
          table, th, td { border: 1px solid black; }
          th, td { padding: 8px; text-align: left; }
          th { background-color: #f2f2f2; }
        </style>
      </head>
      <body>
        <h2>Generated Q&A</h2>
        <table>
          <thead>
            <tr>
              <th>Question</th>
              <th>Answer</th>
            </tr>
          </thead>
          <tbody>
            ${generatedQA.map(row => `
              <tr>
                <td>${row[0]}</td>
                <td>${row[1]}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </body>
      </html>
    `;

  
    printJS({ printable: printContent, type: 'raw-html' });
  };
  const handleExportCSV = () => {
    const csvData = generatedQA.map(row => `${row[0]},${row[1]}`).join('\n');
    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generatedQA.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportExcel = () => {
    const ws = XLSX.utils.json_to_sheet(generatedQA.map(row => ({
      Question: row[0],
      Answer: row[1],
    })));
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    saveAs(new Blob([wbout], { type: 'application/octet-stream' }), 'generatedQA.xlsx');
  };

  const handleExportPDF = () => {
    const docDefinition = {
      content: [
        { text: 'Generated Q&A', style: 'header' },
        {
          table: {
            body: [
              ['Question', 'Answer'],
              ...generatedQA.map(row => [row[0], row[1]]),
            ]
          }
        }
      ],
      styles: {
        header: {
          fontSize: 18,
          bold: true,
          margin: [0, 0, 0, 10]
        },
        table: {
          margin: [0, 5, 0, 15]
        },
        tableHeader: {
          bold: true,
          fontSize: 13,
          color: 'black'
        },
      }
    };
    pdfMake.createPdf(docDefinition).download('generatedQA.pdf');
  };

  return (
    <div className="container mt-4">
      {generatedQA.length > 0 ? (
        <>
          <div className="mb-3">
            <button onClick={handleExportCSV} className="btn btn-primary mr-2">Export to CSV</button>
            <button onClick={handleExportExcel} className="btn btn-primary mr-2">Export to Excel</button>
            <button onClick={handleExportPDF} className="btn btn-primary mr-2">Export to PDF</button>
            <button onClick={handlePrint} className="btn btn-primary">Print</button>
          </div>
          <div className="hidden">
          <DataTable
            title="Generated Q&A"
            columns={columns}
            data={generatedQA}
            pagination
            selectableRows
          />
          </div>
          <GeneratedQA data={generatedQA} />
        </>
      ) : (
        <p>No results to display</p>
      )}
    </div>
  );
}

export default GeneratedPage;
