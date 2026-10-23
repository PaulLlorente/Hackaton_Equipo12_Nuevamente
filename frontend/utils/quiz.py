import re


def formatear_opciones(texto: str | list) -> list[str]:
    if isinstance(texto, list):
        return [str(op).strip() for op in texto if str(op).strip()]

    if not isinstance(texto, str) or not texto.strip():
        return []

    opciones = re.split(r"(?=[A-D][\.\)])", texto)
    return [op.strip() for op in opciones if op.strip()]
