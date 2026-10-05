from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.src.ingestion.main import procesar_documento
from backend.src.nuevamente_rag.pipeline import search_index, SentenceTransformerEmbedder
from backend.src.nuevamente_rag.vector_store import MotorVectorialRAG
router = APIRouter(tags=["RAG Engine"])

# ==============================================================================
# SEGURIDAD JWT
# ==============================================================================
# RAG ENGINE (Preparado para el consumo y el LLM)
# ==============================================================================

# --- Inicialización de Modelos ---
embedder = SentenceTransformerEmbedder()

class SearchRequest(BaseModel):
    query: str
    index_dir: str = "data/index"
    top_k: int = 3
    tenant_id: Optional[str] = None

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "NuevaMente API"}

@router.post("/api/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    document_id: str = Form(...),
    # TODO: Descomentar para proteger la ruta
    # _usuario: dict = Depends(obtener_usuario)
):
    try:
        # LECTURA EN MEMORIA
        contenido_bytes = await file.read()

        nombre_archivo_seguro: str = file.filename or "documento_desconocido.pdf"

        # EXTRACCIÓN (Recibe el string gigante limpio desde el PDF)
        texto_crudo = procesar_documento(
            source=contenido_bytes,
            nombre_archivo=nombre_archivo_seguro,
            tenant_id=tenant_id,
            document_id=document_id
        )

        # MOTOR VECTORIAL RAG
        motor_rag = MotorVectorialRAG()
        motor_rag.ingestar_y_vectorizar_memoria(
            texto_crudo=texto_crudo,
            tenant_id=tenant_id,
            document_id=document_id,
            origen=nombre_archivo_seguro
        )

        return {
            "status": "success",
            "document_id": document_id,
            "tenant_id": tenant_id,
            "mensaje": "Documento procesado, segmentado y vectorizado correctamente."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/search")
def search(
    request: SearchRequest,
    # TODO ERICK: Descomentar para proteger la ruta
    # _usuario: dict = Depends(obtener_usuario)
):
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