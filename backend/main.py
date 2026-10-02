from fastapi import FastAPI
from backend.src.api.routers import generar_contenido
from backend.src.nuevamente_rag.api import router as rag_router

# Para levantar el servidor local usa el comando: python -m uvicorn backend.main:app --reload

app = FastAPI(
    title="NuevaMente API Monorepo",
    version="1.0.0",
    description="API unificada para Ingestión, Búsqueda Semántica y Generación"
)

# Registro de routers
app.include_router(generar_contenido.router)
# Conecta tus endpoints de ingestión y búsqueda
app.include_router(rag_router)