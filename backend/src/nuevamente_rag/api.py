from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel
import logging

from backend.src.ingestion.main import procesar_documento
from backend.database.schema_db import Users
from backend.src.nuevamente_rag.vector_store import MotorVectorialRAG
from backend.src.administrar_usuarios.gestionar_usuario import obtener_usuario

router = APIRouter(tags=["RAG Engine"])

# ==============================================================================
# SEGURIDAD JWT
# ==============================================================================
# RAG ENGINE (Preparado para el consumo y el LLM)
# ==============================================================================

# --- logging para debugging ---
logger = logging.getLogger(__name__)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3
    tenant_id: str


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "NuevaMente API"}


@router.post("/api/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    document_id: str = Form(...),
    usuario: Users = Depends(obtener_usuario),
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
            document_id=document_id,
        )

        # MOTOR VECTORIAL RAG
        motor_rag = MotorVectorialRAG()
        motor_rag.ingestar_y_vectorizar_memoria(
            texto_crudo=texto_crudo,
            tenant_id=tenant_id,
            document_id=document_id,
            origen=nombre_archivo_seguro,
        )

        return {
            "status": "success",
            "document_id": document_id,
            "tenant_id": tenant_id,
            "mensaje": "Documento procesado, segmentado y vectorizado correctamente.",
        }
    except Exception as e:
        logger.exception("Error al procesar el documento:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/search")
def search(request: SearchRequest, usuario: Users = Depends(obtener_usuario)):
    try:
        motor_rag = MotorVectorialRAG()
        results = motor_rag.recuperar_contexto(
            query=request.query,
            tenant_id=request.tenant_id,
            k=request.top_k,
        )
        return {
            "status": "success",
            "query": request.query,
            "total_results": len(results),
            "results": results,
        }
    except Exception as e:
        logger.exception("Error al buscar documentos:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))