import React from 'react';
import { useNavigate } from 'react-router-dom';
import QuestionForm from './QuestionForm';
import axios from 'axios';

function QuestionPage() {
  const [generatedQA, setGeneratedQA] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const navigate = useNavigate();
console.log(generatedQA);
  const handleFormSubmit = async (inputText, testType, noOfQues) => {
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5001/test_generate', {
        itext: inputText,
        test_type: testType,
        noq: noOfQues,
      });
      setGeneratedQA(response.data.cresults);
      navigate('/generated', { state: { data: response.data.cresults } });
    } catch (error) {
      console.error('There was an error generating the test data!', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      {loading ? (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
          <div className="loader">Loading...</div>
        </div>
      ) : (
        <QuestionForm onFormSubmit={handleFormSubmit} />
      )}
    </div>
  );
}

export default QuestionPage;
