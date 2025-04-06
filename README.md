# 🩺 AI-Powered Medical Report Summarizer & Explainer

This microSaaS app uses **GPT-4 Vision** or optionally **Mistral-med LLMs** to analyze and explain scanned medical reports (e.g., CBC, MRI, X-ray results). Built using **Streamlit** for frontend and **Flask** as an API backend, it supports both PDF and image uploads.

---

## ✨ Features
- Upload medical reports in PDF or image format
- AI reads and understands complex medical reports
- Generates a human-friendly explanation:
  - Key findings
  - Patient-friendly summary
  - Suggested next steps

---

## 📁 Project Structure
```
medical-report-summarizer/
├── streamlit_app.py                # Streamlit frontend
├── medical_api.py                  # Flask backend API
├── Dockerfile                      # Docker container config
├── requirements.txt                # All Python dependencies
├── README.md                       # Project overview
├── .env                            # Contains your OPENAI_API_KEY
```

---

## ⚙️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Flask + Flask-CORS + Flasgger (Swagger UI)
- **LLM:** GPT-4-Vision (`gpt-4-1106-vision-preview`) or Mistral (optional)
- **PDF/Image Parsing:** PyMuPDF (fitz), PIL
- **Deployment:** Docker

---

## 🚀 Setup Instructions

### 🔧 1. Clone the repo
```bash
git clone https://github.com/yourname/medical-report-summarizer.git
cd medical-report-summarizer
```

### 📦 2. Install dependencies (locally)
```bash
pip install -r requirements.txt
```

### 🔐 3. Add OpenAI Key in `.env`
```
OPENAI_API_KEY=sk-xxxxxx
```

---

## 🖼️ Streamlit App (Frontend)
Run:
```bash
streamlit run streamlit_app.py
```
Go to: [http://localhost:8501](http://localhost:8501)

---

## 🧠 Flask API (Backend)
Run:
```bash
python medical_api.py
```
Visit Swagger: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

---

## 🐳 Docker Setup
### 🏗️ Build the image:
```bash
docker build -t medical-ai-api .
```
### ▶️ Run the container:
```bash
docker run --env-file .env -p 5000:5000 medical-ai-api
```

---

## 📥 Example cURL Request
```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@./sample_mri_report.pdf"
```

---

## 📌 Future Features
- Integration with WhatsApp or email
- Add OCR enhancement for handwriting
- Use medical-specific models like BioGPT, ClinicalBERT, Mistral-med

---

## 👨‍⚕️ Built For
- Clinics and Diagnostic Labs
- Patients who want simplified explanations
- Health-tech SaaS providers

---

## 🧠 Powered By
- OpenAI GPT-4 Vision
- PyMuPDF
- Flask + Streamlit
- Docker

---

Made with 💊 by Virendra

