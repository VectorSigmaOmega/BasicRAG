# Knowledge-base Search Engine (RAG)

<img width="1230" height="624" alt="Screenshot 2026-04-03 122014" src="https://github.com/user-attachments/assets/1b2c9347-6cb3-4381-aaf0-71817552c137" />


A Retrieval-Augmented Generation (RAG) system to search across multiple text/PDF documents and synthesize answers to user queries using the Google Gemini API.

## Architecture

*   **Backend:** Python + FastAPI
*   **Vector Database:** FAISS (In-memory, ephemeral)
*   **Embeddings & LLM:** Google Gemini (`gemini-3-flash-preview` and `gemini-embedding-2-preview` with automatic fallback).
*   **Frontend:** React (Vite) + Vanilla CSS

This system is designed to have **minimal local dependencies**. FAISS runs entirely in-memory, and all heavy ML computation (embeddings and synthesis) is offloaded to the Google Gemini API. No local Docker containers or PostgreSQL installations are required.

## Prerequisites

*   Python 3.9+
*   Node.js 18+
*   A Google Gemini API Key

---

## 1. Backend Setup

The backend handles document ingestion, text chunking, FAISS vector storage, and interacting with the Gemini API.

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the FastAPI server:
    ```bash
    python main.py
    ```
    The API will be available at `http://localhost:8000`.

---

## 2. Frontend Setup

The frontend provides a clean, professional React interface to input your API key, upload documents, and ask questions.

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173`.

---

## Usage Instructions

1.  Open the frontend application in your browser (`http://localhost:5173`).
2.  In the left sidebar, paste your **Google Gemini API Key**. (It is stored securely in your browser's local storage and passed in the headers of API requests. It is never logged or stored on the backend).
3.  Click **Upload Document** and select a PDF or Text file. Wait for the success message confirming the document was chunked and indexed.
4.  Use the main chat area to ask questions about the uploaded documents. The LLM will synthesize an answer, and you can click "Show Sources" to view the specific chunks of text it used.

## Design Constraints Addressed

*   **Minimal Dependencies:** Avoided heavy database systems (Postgres/Milvus) by using purely in-memory FAISS.
*   **No Hardcoded Secrets:** The API key is provided dynamically via the UI.
*   **Aesthetics:** Used standard CSS variables and a flexbox layout to create a modern, clean, custom UI without relying on generic template libraries.
