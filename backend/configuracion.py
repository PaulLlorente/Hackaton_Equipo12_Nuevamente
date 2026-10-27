import os
from pathlib import Path
from dotenv import load_dotenv

# Obtiene la ruta de la carpeta donde está este archivo (backend/)
BASE_DIR = Path(__file__).resolve().parent

# Carga explícitamente el archivo .env ubicado dentro de backend/
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Obtiene las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")