// frontend/src/pages/Index.jsx
import { useNavigate } from 'react-router-dom';
import './Index.css'; // Make sure your CSS is imported

export default function Index() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const mode = e.target.mode.value;
    const media = e.target.media.value;
    navigate(`/form?mode=${mode}&media=${media}`);
  };

  return (
    <div className="container">
      <div className="form_area">
        <p className="title">STEGANOGRAPHY TOOL</p>
        <form onSubmit={handleSubmit}>
          <div className="form_group">
            <label className="sub_title" htmlFor="mode">Select Mode:</label>
            <select className="form_style" name="mode" id="mode">
              <option value="encode">Encode</option>
              <option value="decode">Decode</option>
            </select>
          </div>
          <div className="form_group">
            <label className="sub_title" htmlFor="media">Media:</label>
            <select className="form_style" name="media" id="media">
              <option value="text">Text</option>
              <option value="image">Image</option>
              <option value="audio">Audio</option>
              <option value="video">Video</option>
            </select>
          </div>
          <div>
            <button className="btn" type="submit">Continue</button>
          </div>
        </form>
      </div>
    </div>
  );
}
