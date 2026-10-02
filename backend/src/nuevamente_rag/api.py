import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

from backend.src.ingestion.main import procesar_documento
from backend.src.nuevamente_rag.pipeline import search_index, SentenceTransformerEmbedder
from backend.src.nuevamente_rag.vector_store import MotorVectorialRAG

router = APIRouter(tags=["RAG Engine"])

# --- Configuración de Seguridad JWT ---
SUPABASE_JWT_SECRET: str = str(os.getenv("SUPABASE_JWT_SECRET", "super-secret-jwt-token-placeholder"))
ALGORITHMS: list[str] = ["HS256"]
security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Valida el token de Supabase en cada petición protegida."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=ALGORITHMS, options={"verify_aud": False})
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, alterado o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
    # Descomenta la siguiente línea cuando quieras activar la seguridad JWT para probar
    # _usuario: dict = Depends(verificar_token)
):
    try:
        #  LECTURA EN MEMORIA
        contenido_bytes = await file.read()

        nombre_archivo_seguro: str = file.filename or "documento_desconocido.pdf"

        # EXTRACCIÓN (Recibe el string gigante limpio desde el PDF)
        texto_crudo = procesar_documento(
            source=contenido_bytes,
            nombre_archivo=nombre_archivo_seguro,
            tenant_id=tenant_id,
            document_id=document_id
        )

        #  MOTOR VECTORIAL RAG
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
    # Descomenta la siguiente línea cuando quieras activar la seguridad JWT
    # _usuario: dict = Depends(verificar_token)
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