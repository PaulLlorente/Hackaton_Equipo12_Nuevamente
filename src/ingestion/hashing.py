import hashlib
from pathlib import Path

# Función que calcula el hash SHA-256 del archivo original.
# El archivo se lee en bloques de 1 MB para optimizar el uso de memoria.
def calcular_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
