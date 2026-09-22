from fastapi import FastAPI
from backend.app.routers import generar_contenido

#Para levantar el servidor local usa el comando uvicorn backend.app.main:app --reload

app = FastAPI()

#Registro routers
app.include_router(generar_contenido.router)

