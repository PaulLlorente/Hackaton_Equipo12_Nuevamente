import hashlib

# Función que calcula el hash SHA-256 del archivo original.
# Calcula el hash directamente desde los bytes del archivo. 
def calcular_sha256(source: bytes) -> str:
    sha256 = hashlib.sha256()
    sha256.update(source)
    return sha256.hexdigest()
