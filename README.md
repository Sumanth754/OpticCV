# 📄 NexusDocs: Production-Grade RAG (AI Document Assistant)

NexusDocs is a powerful **Retrieval-Augmented Generation (RAG)** application that allows you to chat with your PDF documents locally or in the cloud. It features a dual-engine system using **FAISS** for vector search and **Google Gemini** for high-quality AI responses.

---

## 🚀 Key Features
- **Smart RAG:** Chat with your resumes, reports, and PDFs.
- **Hybrid Search:** Combines semantic (FAISS) and keyword (BM25) search for high accuracy.
- **Free AI Engine:** Integrated with **Google Gemini (gemini-flash-latest)** for free, fast, and optimal answers.
- **Local Fallback:** Works even when offline by extracting direct snippets from your documents.

## 🛠️ Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **AI Framework:** [LangChain](https://www.langchain.com/)
- **Database:** [FAISS](https://github.com/facebookresearch/faiss) (Vector Store)
- **Model:** Google Gemini (1.5 Flash)

---

## 🏗️ Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key (Get it free at [Google AI Studio](https://aistudio.google.com/))

### 2. Installation
```bash
git clone https://github.com/YOUR_USERNAME/NexusDocs.git
cd NexusDocs
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Environment
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the Project
```bash
python run_project.py
```
This will start the **Backend (Port 7777)** and **UI (Port 8501)** automatically.

---

## 🌐 Free Deployment (Streamlit Cloud)
To get a **working link** for your GitHub:
1. Push this code to a public GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Connect your repo and set the main file to `ui/app.py`.
4. In the "Advanced Settings," add your `GOOGLE_API_KEY` under the **Secrets** section.

---

## 📄 License
This project is open-source and free to use.
