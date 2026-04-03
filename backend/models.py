from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    context_chunks: List[str]

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_count: int
