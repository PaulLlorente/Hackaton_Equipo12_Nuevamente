from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de los routers
from backend.src.api.routers import generar_contenido
from backend.src.nuevamente_rag import api as rag_api

app = FastAPI(
    title="NUEVAMENTE EQUIPO 12",
    description="API-Adaptación Y Generación De Contenido",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que el frontend se conecte sin bloqueos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de los enrutadores
app.include_router(generar_contenido.router)
app.include_router(rag_api.router)