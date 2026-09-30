from pydantic import BaseModel
from typing import Optional

#Esquema para validar los datos de registro de un usuario
class Registro(BaseModel):
    email:str
    password:str

#Esquema para validar los datos de inicio de sesión
class Login(BaseModel):
    email:str
    password:str

#Esquema para validar los datos que se pueden actualizar
class ActualizarDatos(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


