from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta,timezone
from typing import Optional
from backend.configuracion import SECRET_KEY,ALGORITHM

#Configura el algoritmo utilizado para generar y verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Genera un hash seguro a partir de la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Verifica si la contraseña coincide con el hash almacenado
def validar_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

#Genera un token de acceso con una fecha de expiración
def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
    
    to_encode.update({"exp": int(expire.timestamp())})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





