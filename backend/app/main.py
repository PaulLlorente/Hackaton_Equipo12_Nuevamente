from fastapi import FastAPI
from backend.app.routers import generar_contenido
from backend.app.routers import usuario

#Para levantar el servidor local usa el comando uvicorn backend.app.main:app --reload

app = FastAPI()

#Registro routers

#Apis de generacion de contenido
app.include_router(generar_contenido.router)

#Apis que gestionan el login
app.include_router(usuario.router)

