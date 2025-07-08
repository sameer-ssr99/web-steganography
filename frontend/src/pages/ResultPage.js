import React from 'react';
import { useLocation } from 'react-router-dom';
import './Result.css'; // Optional if you're using a shared CSS file

function ResultPage() {
  const location = useLocation();
  const { message } = location.state || {};

  return (
    <div className="container">
      <div className="form_area">
        <p className="title">DECODED RESULT</p>
        <div className="form_group">
          <label className="sub_title">Hidden Message:</label>
          <div className="form_style" style={{ wordWrap: 'break-word', whiteSpace: 'pre-wrap' }}>
            {message || 'No message found.'}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultPage;
