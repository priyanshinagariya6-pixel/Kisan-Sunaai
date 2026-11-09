>>>>>>> origin/main
# 🌾 Kisan Sunaai – AI-Powered Farmer Complaint Assistant

Kisan Sunaai is a voice-first AI-powered platform designed to help farmers in India submit and understand their agricultural complaints in a simple and accessible way.

Farmers can record their complaints in Hindi. The system converts speech into text, analyzes the complaint using AI, generates a complaint record, and provides a Hindi voice response.

## ✨ Features

- 🎙️ Voice-based complaint recording
- 🇮🇳 Hindi speech-to-text using Gnani AI Prisma
- 🤖 AI-powered complaint analysis using Google Gemini
- 📂 Automatic complaint record storage
- 🆔 Unique complaint tracking ID
- 🔊 Hindi voice responses using Gnani AI Timbre
- 🔎 Complaint tracking
- 🌱 Farmer-friendly interface

## 🛠️ Technologies Used

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- FastAPI

**AI Services**
- Gnani AI (Speech-to-Text and Text-to-Speech)
- Google Gemini API
- Hugging Face Transformers

## ⚙️ Project Structure

```text
KisanSunaai/
│
├── backend/
│   ├── api.py
│   ├── complaint_pipeline.py
│   ├── save_complaint.py
│   └── track_complaint.py
│
├── frontend/
│   └── index.html
│
├── .gitignore
└── README.md
```

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd KisanSunaai
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi uvicorn python-multipart python-dotenv
=======
# Kisan-Sunaai
AI-powered Hindi voice assistant for farmer grievance analysis and complaint tracking.
>>>>>>> 781998406b68e382cf36f4a35e8e978cc9e90fa6
