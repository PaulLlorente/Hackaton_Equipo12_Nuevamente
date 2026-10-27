from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.configuracion import DATABASE_URL

# Crea el motor agregando pool_pre_ping y pool_recycle para evitar desconexiones de Supabase
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verifica que la conexión esté viva antes de enviar la consulta
    pool_recycle=240 ,   # Recicla las conexiones cada 5 minutos
    pool_timeout=30,     # Parámetro crítico para Supabase
    pool_size=5,
    max_overflow=10
)

# Crea la sesión
Session = sessionmaker(bind=engine)

# Crea una sesión y garantiza que se cierre al terminar
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()