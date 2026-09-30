import jwt
from backend.app.database.schema_db import Users
from backend.app.database.conexión_db import get_db
from backend.app.services.administrar_usuarios.auth import hash_password,validar_password,crear_token_acceso
from backend.app.configuracion import SECRET_KEY,ALGORITHM
from sqlalchemy import select
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer


#Configura la autenticación mediante tokens Bearer
usuario_token = OAuth2PasswordBearer(tokenUrl="/usuario/login")


#Registra un nuevo usuario en la base de datos
def registro(db,Datos):
    stmt = select(Users).where(Users.email == Datos.email)
    usuario_existente = db.scalar(stmt)

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    else:
        password = hash_password(Datos.password)
        usuario = Users(
                email = Datos.email,
                password = password
            )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)


#Verifica las credenciales del usuario y genera un token de acceso
def login(db,Datos):
    usuario = db.scalar(select(Users).where(Users.email == Datos.email))

    if not usuario or not validar_password(Datos.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_de_acceso = crear_token_acceso(
        data={"sub": usuario.email, "rol": usuario.rol}
    )

    return {
        "access_token": token_de_acceso,
        "token_type": "bearer",
        "rol": usuario.rol
    }

#Actualiza el correo o la contraseña del usuario
def actualizar_datos(db, usuario_actual: Users, Datos):
    if Datos.email and Datos.email != usuario_actual.email:
        usuario_existente = db.scalar(select(Users).where(Users.email == Datos.email))
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya está en uso por otra cuenta"
            )
        usuario_actual.email = Datos.email

    if Datos.password:
        usuario_actual.password = hash_password(Datos.password)

    db.commit()
    db.refresh(usuario_actual)
    

#Valida el token y obtiene al usuario autenticado
def obtener_usuario(token: str = Depends(usuario_token), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido"
            )
    except jwt.PyJWTError:  # Captura errores relacionados con la validación del token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token expirado o inválido"
        )

    usuario = db.scalar(select(Users).where(Users.email == email))
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no encontrado"
        )

    return usuario