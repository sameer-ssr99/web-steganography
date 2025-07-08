# 🕵️‍♂️ Web Steganography Tool

A full-stack web application that allows users to **hide (encode)** and **extract (decode)** secret messages within various types of media files, including **images, audio, video, and text** — all through a simple and intuitive interface.

🌐 **Live Demo:** [https://web-steganography-6waw.vercel.app](https://web-steganography-6waw.vercel.app)

---

## ✨ Features

- 🔐 Encode messages into:
  - Images
  - Audio files
  - Video files
  - Text documents
- 🕵️ Decode hidden messages from uploaded media
- 📦 Download encoded files after processing
- 🎯 Clean and responsive UI
- 🔁 Supports both frontend and backend deployment

---

## 🛠️ Tech Stack

### 🔹 Frontend
- React.js
- React Router
- HTML5 + CSS3
- **Vercel** (for deployment)

### 🔹 Backend
- Flask (Python)
- Flask-CORS
- OpenCV, PIL, Stegano
- **Render.com** (for deployment)

---

## 📂 Project Structure

web-steganography/  
├── frontend/          # React frontend  
│   └── src/pages/  
│       ├── FormPage.js  
│       ├── IndexPage.js  
│       └── ResultPage.js  
├── backend/           # Flask backend  
│   ├── app.py  
│   ├── libs/  
│   │   ├── image_steganography.py  
│   │   ├── audio_steganography.py  
│   │   ├── video_steganography.py  
│   │   └── text_steganography.py  
│   └── requirements.txt

---

## 🚀 How to Run Locally

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/sameer-ssr99/web-steganography.git
cd web-steganography
\`\`\`

### 2. Set up the Backend
\`\`\`bash
cd backend
pip install -r requirements.txt
python app.py
\`\`\`
By default, Flask will run at: `http://localhost:5000`

### 3. Set up the Frontend
Open a new terminal:
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`
React app will run at: `http://localhost:3000`

✅ Create a `.env` file inside `frontend/` and add:
\`\`\`env
REACT_APP_API_URL=http://localhost:5000
\`\`\`

---

## 🧠 Educational Disclaimer

> ⚠️ This project is developed **strictly for educational and academic purposes only**.  
> It should **not be used** for any malicious, unauthorized, or illegal data concealment.

---

## 🙌 Acknowledgements

- [OpenCV](https://opencv.org/)
- [Pillow (PIL)](https://pillow.readthedocs.io/)
- [Stegano](https://pypi.org/project/stegano/)
- [Flask](https://flask.palletsprojects.com/)
- [React](https://reactjs.org/)

---

## 📧 Contact

If you'd like to connect, feel free to reach me via GitHub:  
👉 [@sameer-ssr99](https://github.com/sameer-ssr99)
