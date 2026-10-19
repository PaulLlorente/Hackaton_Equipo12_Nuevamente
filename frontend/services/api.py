import os
import uuid
from pathlib import Path

import requests
import streamlit as st

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

MENSAJE_SIN_CONEXION = (
    "No se pudo conectar con el backend. Verifica que FastAPI esté ejecutándose."
)
MENSAJE_SESION_EXPIRADA = "Tu sesión expiró o no es válida. Inicia sesión de nuevo."


def obtener_headers():
    token = st.session_state.get("token")

    if not token:
        return {}

    return {"Authorization": f"Bearer {token}"}


def formatear_detalle(detalle):
    """Convierte el campo `detail` de FastAPI en un texto legible.

    En errores de validación (422) FastAPI devuelve una lista de objetos
    {"loc": [...], "msg": "..."}; en el resto, normalmente un string.
    """
    if not isinstance(detalle, list):
        return str(detalle)

    mensajes = []

    for error in detalle:
        if not isinstance(error, dict):
            mensajes.append(str(error))
            continue

        campo = ".".join(str(parte) for parte in error.get("loc", []) if parte != "body")
        mensaje = error.get("msg", "valor inválido")
        mensajes.append(f"{campo}: {mensaje}" if campo else mensaje)

    return "; ".join(mensajes)


def procesar_respuesta(respuesta):
    try:
        datos = respuesta.json()
    except ValueError:
        datos = respuesta.text

    if respuesta.ok:
        return True, datos

    if isinstance(datos, dict):
        return False, formatear_detalle(datos.get("detail", datos))

    return False, str(datos)


def _peticion(metodo, ruta, *, requiere_token=True, timeout=30, **kwargs):
    """Punto único de salida hacia el backend.

    Devuelve siempre (exito, resultado): `resultado` son los datos si hubo
    éxito, o un mensaje legible para el usuario si falló.
    """
    if requiere_token and not st.session_state.get("token"):
        return False, "Debes iniciar sesión para realizar esta acción."

    headers = obtener_headers() if requiere_token else {}

    try:
        respuesta = requests.request(
            metodo,
            f"{API_URL}{ruta}",
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    except requests.exceptions.ConnectionError:
        return False, MENSAJE_SIN_CONEXION

    except requests.exceptions.Timeout:
        return False, f"El servidor tardó más de {timeout} segundos en responder."

    except requests.exceptions.RequestException as error:
        return False, f"Error de comunicación con el servidor: {error}"

    # Un 401 en una ruta protegida significa token vencido o inválido.
    # En login/registro NO aplica: ahí un 401 son credenciales incorrectas.
    if respuesta.status_code == 401 and requiere_token:
        st.session_state.token = None
        return False, MENSAJE_SESION_EXPIRADA

    return procesar_respuesta(respuesta)


def iniciar_sesion(email, password):
    return _peticion(
        "POST",
        "/usuario/login",
        requiere_token=False,
        json={"email": email, "password": password},
    )


def registrar_usuario(email, password):
    return _peticion(
        "POST",
        "/usuario/registro",
        requiere_token=False,
        json={"email": email, "password": password},
    )


def cargar_documento(archivo, tenant_id):
    nombre_archivo = Path(archivo.name).stem
    document_id = f"{nombre_archivo}_{uuid.uuid4().hex[0:8]}"

    archivo.seek(0)

    exito, resultado = _peticion(
        "POST",
        "/api/ingest",
        timeout=180,
        files={
            "file": (
                archivo.name,
                archivo,
                archivo.type or "application/octet-stream",
            )
        },
        data={"tenant_id": tenant_id, "document_id": document_id},
    )

    if exito:
        if isinstance(resultado, dict):
            resultado.setdefault("document_id", document_id)
            resultado.setdefault("tenant_id", tenant_id)
        else:
            resultado = {
                "document_id": document_id,
                "tenant_id": tenant_id,
                "respuesta": resultado,
            }

    return exito, resultado


def consultar_rag(pregunta, tenant_id, top_k=3):
    return _peticion(
        "POST",
        "/api/search",
        timeout=120,
        json={"query": pregunta, "tenant_id": tenant_id, "top_k": top_k},
    )


def adaptar_contenido(query, tenant_id, perfil, formato, top_k=3, cantidad_items=3):
    return _peticion(
        "POST",
        "/adaptar",
        timeout=120,
        json={
            "query": query,
            "tenant_id": tenant_id,
            "perfil": perfil,
            "formato": formato,
            "top_k": top_k,
            "cantidad_items": cantidad_items,
        },
    )
