import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

API_URL = os.getenv("API_URL")

if not API_URL:
    raise RuntimeError(
        "La variable de entorno API_URL no está definida en el archivo .env"
    )

API_URL = API_URL.rstrip("/")
