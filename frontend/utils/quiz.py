import re

def formatear_opciones(texto:str)->list[str]:
    opciones = re.split(r'(?=[A-D][\.\)])', texto)

    opciones_limpias = [op.strip() for op in opciones if op.strip()]
    
    return opciones_limpias
    