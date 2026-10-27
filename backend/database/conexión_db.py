from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ruta absoluta hacia la base de datos app.db dentro de backend/database/
BASE_DIR = Path(__file__).resolve().parent.parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/database/app.db"

# Configuración del motor con parámetros de resiliencia
# Nota: connect_args es específico para SQLite; si usas Supabase/PostgreSQL, 
# puedes omitir check_same_thread y ajustar los argumentos del pool.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_recycle=3600,     # Recicla conexiones para evitar cierres por inactividad
    pool_timeout=30        # Tiempo de espera máximo (segundos) para liberar o tomar una conexión
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()