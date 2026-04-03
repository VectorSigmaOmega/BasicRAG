import fitz  # PyMuPDF
import faiss
import numpy as np
from google import genai
from google.genai import types
from typing import List
import os

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.dimension = None  # Will be set dynamically based on the embedding model
        self.index = None
        self.chunks: List[str] = []
        
    def _chunk_text(self, text: str) -> List[str]:
        """Splits text into chunks with overlap."""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
            
        return chunks

    def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extracts text from a PDF or plain text file."""
        text = ""
        if filename.lower().endswith('.pdf'):
            doc = fitz.open(stream=file_content, filetype="pdf")
            for page in doc:
                text += page.get_text()
        else:
            text = file_content.decode('utf-8', errors='ignore')
        return text

    def get_embeddings(self, texts: List[str], api_key: str, task_type: str = 'RETRIEVAL_DOCUMENT') -> np.ndarray:
        """Gets embeddings from Google Gemini API."""
        client = genai.Client(api_key=api_key)
        
        # Fallback list of models, starting with the preview model the user suggested
        models_to_try = ['gemini-embedding-2-preview', 'gemini-embedding-001']
        
        embeddings = []
        batch_size = 20 # Limit batch size to avoid payload size/rate limit errors
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            success = False
            last_err = None
            
            for model in models_to_try:
                try:
                    response = client.models.embed_content(
                        model=model,
                        contents=batch,
                        # We omit task_type as some preview/older models might reject it
                    )
                    
                    batch_embs = [emb.values for emb in response.embeddings]
                    embeddings.extend(batch_embs)
                    success = True
                    break # Successful model found, continue to next batch
                except Exception as e:
                    last_err = e
                    continue
            
            if not success:
                raise Exception(f"Failed to embed batch. Last error: {str(last_err)}")
                
        return np.array(embeddings, dtype='float32')

    def process_and_store(self, file_content: bytes, filename: str, api_key: str) -> int:
        """Extracts, chunks, embeds, and stores in FAISS."""
        text = self.extract_text(file_content, filename)
        new_chunks = self._chunk_text(text)
        
        if not new_chunks:
            return 0
            
        embeddings = self.get_embeddings(new_chunks, api_key, task_type='RETRIEVAL_DOCUMENT')
        
        if self.index is None:
            self.dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(self.dimension)
            
        # Add to FAISS index and local chunk storage
        self.index.add(embeddings)
        self.chunks.extend(new_chunks)
        
        return len(new_chunks)

    def search(self, query: str, api_key: str, top_k: int = 3) -> List[str]:
        """Searches the vector database for relevant chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []
            
        # Get query embedding
        query_embeddings = self.get_embeddings([query], api_key, task_type='RETRIEVAL_QUERY')
        query_embedding = query_embeddings[0:1] # shape (1, 768)
            
        # Search FAISS
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])
                
        return results

    def generate_answer(self, query: str, context_chunks: List[str], api_key: str) -> str:
        """Synthesizes an answer using the LLM given the context."""
        client = genai.Client(api_key=api_key)
        
        context_text = "\\n\\n---\\n\\n".join(context_chunks)
        
        prompt = f"""You are a helpful assistant answering questions based ONLY on the provided document context.
If the answer cannot be found in the context, say so. Do not use outside knowledge.

Context:
{context_text}

User Question: {query}
"""
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        return response.text

# Global singleton instance for the in-memory database
processor = DocumentProcessor()
