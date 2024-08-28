import React, { useState } from 'react';

function QuestionForm({ onFormSubmit }) {
  const [inputText, setInputText] = useState('');
  const [testType, setTestType] = useState('objective');
  const [noOfQues, setNoOfQues] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();
    onFormSubmit(inputText, testType, noOfQues);
  };

  return (
    <div className="card border-light shadow-sm p-4">
      <h3 className="text-center">GENERATE QUESTIONS & ANSWERS</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Input Text</label>
          <textarea
            className="form-control"
            rows="6"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            required
          ></textarea>
        </div>
        <div className="form-group">
          <label>Choose Question Type</label>
          <select
            className="custom-select"
            value={testType}
            onChange={(e) => setTestType(e.target.value)}
            required
          >
            <option value="objective">Objective</option>
            <option value="subjective">Subjective</option>
          </select>
        </div>
        <div className="form-group">
          <label>No of Questions</label>
          <input
            type="number"
            className="form-control"
            value={noOfQues}
            onChange={(e) => setNoOfQues(e.target.value)}
            min="1"
            required
          />
        </div>
        <button type="submit" className="btn btn-primary btn-block">Generate</button>
      </form>
    </div>
  );
}

export default QuestionForm;
