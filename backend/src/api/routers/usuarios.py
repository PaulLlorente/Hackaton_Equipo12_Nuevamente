from fastapi import APIRouter,Depends
from backend.src.api.models.schemas_usuario import Registro,Login,ActualizarDatos
from backend.src.administrar_usuarios.gestionar_usuario import registro,login,obtener_usuario,actualizar_datos
from backend.database.conexión_db import get_db
from backend.database.schema_db import Users
from backend.src.api.models.schema_token import TokenValidacion
from backend.src.administrar_usuarios.gestionar_usuario import obtener_usuario


router = APIRouter()


#Registra un nuevo usuario en la base de datos
@router.post("/usuario/registro")
def registrar_usuario(Datos:Registro,db = Depends(get_db)):
    nw_usuario = registro(db,Datos)
    return {"mensaje": "Hola, tu cuenta fue creada. ¡Bienvenido a Nuevamente!"}

#Inicia sesión y genera las credenciales de acceso del usuario
@router.post("/usuario/login",response_model=TokenValidacion)
def iniciar_secion_usuario(Datos:Login,db = Depends(get_db)):
    iniciar_secion = login(db,Datos)
    return iniciar_secion

#Actualiza los datos del usuario autenticado
@router.put("/usuario/actualizar")
def actualizar_datos_usuario(Datos:ActualizarDatos,db = Depends(get_db),usuario: Users = Depends(obtener_usuario)):
    actualizar_datos(db,usuario,Datos)
    return {"mensaje": "Tus Datos se han actualizado"}

#Elimina la cuenta del usuario autenticado
@router.delete("/usuario")
def eliminar_usuario(db = Depends(get_db),usuario: Users = Depends(obtener_usuario)):
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Lamentamos que tengas que irte, tu cuenta fue eliminada."}
    
    