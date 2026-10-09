
import os
import requests
import streamlit as st
import uuid

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def obtener_headers():
    token = st.session_state.get("token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }


def procesar_respuesta(respuesta):
    try:
        datos = respuesta.json()
    except ValueError:
        datos = respuesta.text

    if respuesta.ok:
        return True, datos

    if isinstance(datos, dict):
        return False, str(datos.get("detail", datos))

    return False, str(datos)


def iniciar_sesion(email, password):
    try:
        respuesta = requests.post(
            f"{API_URL}/usuario/login",
            json={
                "email": email,
                "password": password
            },
            timeout=30
        )

        return procesar_respuesta(respuesta)

    except requests.exceptions.RequestException as error:
        return False, str(error)


def registrar_usuario(email, password):
    try:
        respuesta = requests.post(
            f"{API_URL}/usuario/registro",
            json={
                "email": email,
                "password": password
            },
            timeout=30
        )

        return procesar_respuesta(respuesta)

    except requests.exceptions.RequestException as error:
        return False, str(error)


def cargar_documento(archivo, tenant_id):
    if not st.session_state.get("token"):
        return False, "Debes iniciar sesión antes de cargar documentos."

    try:
        document_id = str(uuid.uuid4())

        archivo.seek(0)

        respuesta = requests.post(
            f"{API_URL}/api/ingest",
            headers=obtener_headers(),
            files={
                "file": (
                    archivo.name,
                    archivo,
                    archivo.type or "application/octet-stream"
                )
            },
            data={
                "tenant_id": tenant_id,
                "document_id": document_id
            },
            timeout=180
        )

        exito, resultado = procesar_respuesta(respuesta)

        if exito:
            if isinstance(resultado, dict):
                resultado.setdefault("document_id", document_id)
                resultado.setdefault("tenant_id", tenant_id)
            else:
                resultado = {
                    "document_id": document_id,
                    "tenant_id": tenant_id,
                    "respuesta": resultado
                }

        return exito, resultado

    except requests.exceptions.RequestException as error:
        return False, str(error)


def consultar_rag(pregunta, tenant_id):
    if not st.session_state.get("token"):
        return False, "Debes iniciar sesión antes de consultar documentos."

    try:
        respuesta = requests.post(
            f"{API_URL}/api/search",
            headers=obtener_headers(),
            json={
                "query": pregunta,
                "index_dir": "data/index",
                "top_k": 5,
                "tenant_id": tenant_id
            },
            timeout=120
        )

        return procesar_respuesta(respuesta)

    except requests.exceptions.RequestException as error:
        return False, str(error)


def adaptar_contenido(query, tenant_id, perfil, formato, top_k=3):
    if not st.session_state.get("token"):
        return False, "Debes iniciar sesión antes de adaptar contenido."

    datos = {
        "query": query,
        "tenant_id": tenant_id,
        "perfil": perfil,
        "formato": formato,
        "top_k": top_k
    }

    try:
        respuesta = requests.post(
            f"{API_URL}/adaptar",
            headers=obtener_headers(),
            json=datos,
            timeout=120
        )

        return procesar_respuesta(respuesta)

    except requests.exceptions.ConnectionError:
        return False, (
            "No se pudo conectar con el backend. "
            "Verifica que FastAPI esté ejecutándose."
        )

    except requests.exceptions.Timeout:
        return False, "La adaptación tardó demasiado en responder."

    except requests.exceptions.RequestException as error:
        return False, f"Error de conexión: {error}"
