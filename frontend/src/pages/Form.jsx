import React, { useState } from 'react';
import './Form.css';

const Form = () => {
  const [mode, setMode] = useState('encode');
  const [media, setMedia] = useState('image');
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("mode", mode);
    formData.append("media", media);
    formData.append("file", file);
    formData.append("message", message);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/process`, {
        method: "POST",
        body: formData,
      });

      if (res.headers.get("Content-Type").includes("application")) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "output_file";
        document.body.appendChild(a);
        a.click();
        a.remove();
      } else {
        const html = await res.text();
        document.open();
        document.write(html);
        document.close();
      }
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  return (
    <div className="container">
      <div className="form_area">
        <p className="title">STEGANOGRAPHY TOOL</p>
        <form onSubmit={handleSubmit}>
          <div className="form_group">
            <label className="sub_title" htmlFor="mode">Select Mode:</label>
            <select
              name="mode"
              id="mode"
              className="form_style"
              value={mode}
              onChange={(e) => setMode(e.target.value)}
            >
              <option value="encode">Encode</option>
              <option value="decode">Decode</option>
            </select>
          </div>

          <div className="form_group">
            <label className="sub_title" htmlFor="media">Select Media:</label>
            <select
              name="media"
              id="media"
              className="form_style"
              value={media}
              onChange={(e) => setMedia(e.target.value)}
            >
              <option value="image">Image</option>
              <option value="audio">Audio</option>
              <option value="video">Video</option>
              <option value="text">Text</option>
            </select>
          </div>

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
                name="message"
                className="form_style"
                placeholder="Enter your secret message here..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
              />
            </div>
          )}

          <div>
            <button className="btn" type="submit">SUBMIT</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Form;
