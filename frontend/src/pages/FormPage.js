import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Form.css'; // Ensure your CSS is imported

function FormPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { mode, media } = location.state || {};
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const spinnerStyle = {
    width: '40px',
    height: '40px',
    border: '5px solid #f3f3f3',
    borderTop: '5px solid #3498db',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    margin: '20px auto'
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('mode', mode);
    formData.append('media', media);
    formData.append('file', file);
    if (mode === 'encode') formData.append('message', message);

    setLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/process`, {
        method: 'POST',
        body: formData,
      });

      setLoading(false);

      if (!response.ok) {
        const errorData = await response.json();
        alert("Error: " + errorData.error);
        return;
      }

      if (mode === 'decode') {
        const json = await response.json();
        navigate('/result', { state: { message: json.message || 'No message found.' } });
      } else {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'stego_' + file.name;
        a.click();
      }
    } catch (err) {
      setLoading(false);
      console.error("Error during fetch:", err);
      alert("Something went wrong. Check console for details.");
    }
  };

  return (
    <div className="container">
      <div className="form_area">
        <p className="title">{mode?.toUpperCase()} - {media?.toUpperCase()}</p>
        <form onSubmit={handleSubmit}>
          <div className="form_group">
            <label className="sub_title" htmlFor="file">Choose File:</label>
            <input
              type="file"
              id="file"
              className="form_style"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </div>

          {mode === 'encode' && (
            <div className="form_group">
              <label className="sub_title" htmlFor="message">Text Message:</label>
              <textarea
                id="message"
                className="form_style"
                placeholder="Enter your secret message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                required
              />
            </div>
          )}

          <div>
            <button className="btn" type="submit" disabled={loading}>
              {loading ? 'Processing...' : 'Submit'}
            </button>
          </div>
        </form>

        {loading && <div style={spinnerStyle}></div>}
      </div>
    </div>
  );
}

export default FormPage;
