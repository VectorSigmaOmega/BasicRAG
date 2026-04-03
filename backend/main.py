import traceback
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse, UploadResponse
from document_processor import processor
import uvicorn

app = FastAPI(title="Knowledge-base Search API")

# Setup CORS to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For assignment simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_api_key(x_api_key: str = Header(..., description="Google Gemini API Key")) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key is missing")
    return x_api_key

@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key)
):
    try:
        content = await file.read()
        chunks_added = processor.process_and_store(content, file.filename, api_key)
        return UploadResponse(
            message="Document successfully processed and indexed.",
            filename=file.filename,
            chunks_count=chunks_added
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    api_key: str = Depends(get_api_key)
):
    try:
        if processor.index is None or processor.index.ntotal == 0:
            return QueryResponse(answer="No documents have been uploaded yet. Please upload a document first.", context_chunks=[])
            
        # Retrieve relevant chunks
        context_chunks = processor.search(request.query, api_key)
        
        # Generate answer
        answer = processor.generate_answer(request.query, context_chunks, api_key)
        
        return QueryResponse(answer=answer, context_chunks=context_chunks)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
