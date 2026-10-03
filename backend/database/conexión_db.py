from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.configuracion import DATABASE_URL


#Crea el motor de conexión a la base de datos
engine = create_engine(DATABASE_URL,echo=True)

#Crea el motor de conexión a la base de datos
Session = sessionmaker(bind=engine)

#Crea una sesión y garantiza que se cierre al terminar
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()