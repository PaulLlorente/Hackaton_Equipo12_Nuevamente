import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

from src.ingestion.main import procesar_documento
from src.nuevamente_rag.pipeline import search_index, SentenceTransformerEmbedder
from src.nuevamente_rag.vector_store import MotorVectorialRAG

app = FastAPI(
    title="NuevaMente RAG API",
    version="1.0.0",
    description="API de Ingestión y Búsqueda Semántica con JWT Supabase"
)

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

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "NuevaMente API"}

@app.post("/api/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    document_id: str = Form(...),
    # Descomenta la siguiente línea cuando quieras activar la seguridad JWT para probar
    # _usuario: dict = Depends(verificar_token)
):
    try:
        # 1. LECTURA EN MEMORIA (Asíncrona y sin tocar el disco duro)
        contenido_bytes = await file.read()

        # file.filename puede ser None en FastAPI; garantizamos que siempre sea un string
        nombre_archivo_seguro: str = file.filename or "documento_desconocido.pdf"

        # 2. EXTRACCIÓN (Recibe el string gigante limpio desde el PDF)
        texto_crudo = procesar_documento(
            source=contenido_bytes,
            nombre_archivo=nombre_archivo_seguro,
            tenant_id=tenant_id,
            document_id=document_id
        )

        # 3. DELEGACIÓN AL MOTOR VECTORIAL RAG (La API no hace chunking)
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

@app.post("/api/search")
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