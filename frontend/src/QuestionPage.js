import React from 'react';
import { useNavigate } from 'react-router-dom';
import QuestionForm from './QuestionForm';
import axios from 'axios';

function QuestionPage() {
  const [generatedQA, setGeneratedQA] = React.useState([]);
  const navigate = useNavigate(); 

  const handleFormSubmit = async (inputText, testType, noOfQues) => {
    try {
      const response = await axios.post('http://127.0.0.1:5001/test_generate', {
        itext: inputText,
        test_type: testType,
        noq: noOfQues,
      });
      setGeneratedQA(response.data.cresults);

      navigate(`/generated?data=${encodeURIComponent(JSON.stringify(response.data.cresults))}`);
    } catch (error) {
      console.error('There was an error generating the test data!', error);
    }
  };

  return (
    <div className="container mt-4">
      <QuestionForm onFormSubmit={handleFormSubmit} />
    </div>
  );
}

export default QuestionPage;
