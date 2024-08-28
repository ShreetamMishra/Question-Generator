import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import QuestionPage from './QuestionPage';
import GeneratedPage from './GeneratedPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<QuestionPage />} />
        <Route path="/generated" element={<GeneratedPage />} />
      </Routes>
    </Router>
  );
}

export default App;
