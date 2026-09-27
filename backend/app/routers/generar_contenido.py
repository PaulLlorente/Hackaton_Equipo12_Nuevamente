from fastapi import APIRouter,Depends,UploadFile,Form,HTTPException,status

router = APIRouter()

#Endpoint principal
@router.post("/generar-contenido")
async def generar_contenido(file:UploadFile,perfil: str = Form(...),formato: str = Form(...)):
    pass