import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from src.ingestion.main import procesar_documento
from src.nuevamente_rag.pipeline import search_index, SentenceTransformerEmbedder

app = FastAPI(
    title="NuevaMente RAG API",
    version="1.0.0",
    description="API de Ingestión y Búsqueda Semántica"
)

# Inicializar embedder
embedder = SentenceTransformerEmbedder()

class SearchRequest(BaseModel):
    query: str
    index_dir: str = "data/index"
    top_k: int = 3
    tenant_id: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "NuevaMente API"}

@app.post("/api/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    document_id: str = Form(...)
):
    try:
        temp_dir = Path("data/uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        file_path = temp_dir / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resultado = procesar_documento(
            ruta_archivo=str(file_path),
            tenant_id=tenant_id,
            document_id=document_id
        )

        return {
            "status": "success",
            "document_id": document_id,
            "tenant_id": tenant_id,
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
def search(request: SearchRequest):
    try:
        results = search_index(
            index_dir=request.index_dir,
            query=request.query,
            embedder=embedder,
            top_k=request.top_k,
            tenant_id=request.tenant_id
        )
        return {
            "status": "success",
            "query": request.query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))