import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

from src.ingestion.main import procesar_documento
from src.nuevamente_rag.pipeline import search_index, SentenceTransformerEmbedder

app = FastAPI(
    title="NuevaMente RAG API",
    version="1.0.0",
    description="API de Ingestión y Búsqueda Semántica con JWT Supabase"
)

# ---------------------------------------------------------------------------
# Seguridad y JWT Supabase
# ---------------------------------------------------------------------------
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "super-secret-jwt-token-placeholder")
ALGORITHM = "HS256"

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    rol: str = "usuario"
    tenant_id: Optional[str] = None

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=[ALGORITHM],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception

        rol: str = (
            payload.get("user_metadata", {}).get("rol")
            or payload.get("rol", "usuario")
        )
        tenant_id: Optional[str] = (
            payload.get("user_metadata", {}).get("tenant_id")
            or payload.get("tenant_id")
        )

        return TokenData(user_id=user_id, rol=rol, tenant_id=tenant_id)
    except JWTError:
        raise credentials_exception

# ---------------------------------------------------------------------------
# Inicialización y Modelos
# ---------------------------------------------------------------------------
embedder = SentenceTransformerEmbedder()

class SearchRequest(BaseModel):
    query: str
    index_dir: str = "data/index"
    top_k: int = 3
    tenant_id: Optional[str] = None

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "NuevaMente API"}

@app.post("/api/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    document_id: str = Form(...),
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: solo rol admin puede realizar ingesta"
        )

    try:
        contenido_bytes = await file.read()

        resultado = procesar_documento(
            source=contenido_bytes,
            nombre_archivo=file.filename,
            tenant_id=tenant_id,
            document_id=document_id
        )

        return {
            "status": "success",
            "document_id": document_id,
            "tenant_id": tenant_id,
            "processed_by": current_user.user_id,
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
def search(
    request: SearchRequest,
    current_user: TokenData = Depends(get_current_user)
):
    try:
        tenant = request.tenant_id or current_user.tenant_id

        results = search_index(
            index_dir=request.index_dir,
            query=request.query,
            embedder=embedder,
            top_k=request.top_k,
            tenant_id=tenant
        )
        return {
            "status": "success",
            "query": request.query,
            "user_id": current_user.user_id,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))