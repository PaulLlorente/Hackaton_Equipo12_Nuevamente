from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

#Clase base para los modelos de la base de datos
class Base(DeclarativeBase):
    pass

#Modelo que representa la tabla de usuarios en la base de datos
class Users(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    rol: Mapped[str] = mapped_column(String(255),default="usuario",nullable=False)
    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String(255),nullable=False)



    