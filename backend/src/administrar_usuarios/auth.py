import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from backend.configuracion import SECRET_KEY, ALGORITHM


# Genera un hash seguro directamente con bcrypt
def hash_password(password: str) -> str:
    # bcrypt requiere bytes, por eso codificamos a utf-8
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Lo devolvemos como string para la BD


# Verifica si la contraseña coincide con el hash almacenado
def validar_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# Genera un token de acceso con una fecha de expiración
def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt