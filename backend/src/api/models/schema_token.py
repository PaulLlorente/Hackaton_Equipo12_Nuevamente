from pydantic import BaseModel

#Modelo que representa como debe verse el token
class TokenValidacion(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str