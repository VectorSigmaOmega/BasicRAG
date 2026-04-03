# Project Plan: Knowledge-base Search Engine

## Objective
Build an LLM-based retrieval-augmented generation (RAG) system to search across multiple text/PDF documents and synthesize answers to user queries. 

## Architecture & Tech Stack
- **Backend API:** Python with FastAPI (minimal, lightweight, and excellent for APIs).
- **Document Processing:** `PyMuPDF` (or `PyPDF2`) for parsing PDF documents.
- **Embeddings & Vector Store:**
  - **Embeddings:** Cloud-based API (e.g., Google Gemini or OpenAI) to generate embeddings. This offloads computation, keeping local system overhead minimal.
  - **Vector Store:** `FAISS` (cpu version) or `ChromaDB` running entirely in-memory. This adds virtually no persistent system overhead.
- **LLM Integration:** Cloud-based API (Google Gemini or OpenAI) for answer synthesis. 
  - **Authentication:** The API key will be provided dynamically via the frontend UI by the user and passed securely to the backend for processing.
- **Frontend:** ReactJS (bootstrapped via Vite).
  - Clean, custom, and professional UI/UX, avoiding standard template looks.
  - Includes a settings area to input and temporarily store (in memory/local storage) the LLM API key.

## Deliverables & Tasks

- [ ] **1. Project Setup**
  - [ ] Initialize Git repository on branch `main`.
  - [ ] Setup Python virtual environment (`venv`) for the backend.
  - [ ] Initialize Vite React project for the frontend.
  - [ ] Create a comprehensive `.gitignore` to strictly exclude `node_modules`, `venv`, `.env`, `__pycache__`, build artifacts (`dist/`), and uploaded files.
  - [ ] Create `requirements.txt` for backend and `package.json` for frontend, keeping dependencies minimal.

- [ ] **2. Backend: Document Ingestion API**
  - [ ] Implement text extraction from uploaded PDFs/Text files.
  - [ ] Implement text chunking strategy.
  - [ ] Generate embeddings for text chunks using the provided API key.
  - [ ] Store chunks and embeddings in the in-memory vector database.
  - [ ] Create `POST /api/upload` endpoint for document ingestion (accepting the API key in headers).

- [ ] **3. Backend: Retrieval & Synthesis API**
  - [ ] Implement semantic search in the vector database to retrieve relevant context.
  - [ ] Construct the prompt: *"Using these documents, answer the user’s question succinctly."* combined with retrieved context.
  - [ ] Integrate with LLM API using the provided API key to generate the final answer.
  - [ ] Create `POST /api/query` endpoint for handling user questions (accepting the API key in headers).

- [ ] **4. Frontend (React UI)**
  - [ ] Setup a professional, custom layout with a modern design system (e.g., using standard CSS modules or styled-components to keep it unique, avoiding generic Tailwind templates if requested).
  - [ ] Implement a "Settings" or "Configuration" modal/sidebar to securely paste and save the LLM API key in local browser storage.
  - [ ] Implement document upload interface with progress indicators.
  - [ ] Implement a chat/query interface for asking questions and displaying synthesized answers.
  - [ ] Connect frontend components to backend API endpoints, injecting the API key into request headers.

- [ ] **5. Validation & Refinement**
  - [ ] Test retrieval accuracy with various PDF/text documents.
  - [ ] Verify synthesis quality with the LLM.
  - [ ] Code structure cleanup and linting.
  - [ ] Verify UI/UX feels polished and responsive.

- [ ] **6. Final Deliverables**
  - [ ] Write a detailed `README.md` (setup, run instructions for both frontend and backend).
  - [ ] Verify absolutely no sensitive or temporary files (`node_modules`, API keys) are tracked in Git.
  - [ ] Finalize code for the GitHub Repository on the `main` branch.
  - [ ] (User Action) Record Demo Video.

## Strict Assignment Guidelines Checklist
- [ ] No extra/unnecessary modules committed (e.g., `node_modules`).
- [ ] Only strictly required dependencies used.
- [ ] Branch name is `main`.
- [ ] `.env` and temporary files are ignored.
