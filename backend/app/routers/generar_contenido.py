from fastapi import APIRouter
from fastapi import UploadFile,Form


router = APIRouter()

#Endpoint principal
@router.post("/generar-contenido")
async def generar_contenido(file:UploadFile,perfil: str = Form(...),formato: str = Form(...)):
    pass