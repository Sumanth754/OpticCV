from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import base64
from dotenv import load_dotenv
from src.ingestion.parser import DocumentParser
from src.retrieval.engine import RetrievalEngine
from src.generation.chain import RAGChain
from src.utils.logger import setup_logger

load_dotenv()
logger = setup_logger("API")

app = FastAPI(title="NexusDocs Port 7777")

# Initialize core components
parser = DocumentParser()
engine = RetrievalEngine()
rag = RAGChain()

# Global state
active_retriever = None

class UploadRequest(BaseModel):
    filename: str
    content: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(request: UploadRequest):
    global active_retriever
    try:
        file_content = base64.b64decode(request.content)
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{request.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        chunks = parser.process_pdf(file_path)
        if not chunks:
            raise Exception("No text found.")
        
        active_retriever = engine.get_hybrid_retriever(chunks)
        return {"message": "System Ready"}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_docs(request: QueryRequest):
    global active_retriever
    if not active_retriever:
        raise HTTPException(status_code=400, detail="Please upload a PDF.")
    
    # This call now has a guaranteed internal fallback
    result = rag.ask(active_retriever, request.query)
    return {
        "answer": result["answer"],
        "engine": result["engine"],
        "source_documents": [d.page_content[:200] + "..." for d in result["context"]]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)
