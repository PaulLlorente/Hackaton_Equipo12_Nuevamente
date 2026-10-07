import os
import uuid
import requests
import streamlit as st


API_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)


def obtener_error(respuesta):
    try:
        datos = respuesta.json()

        if isinstance(datos, dict):
            if "detail" in datos:
                detalle = datos["detail"]

                if isinstance(detalle, list):
                    mensajes = []

                    for error in detalle:
                        if isinstance(error, dict):
                            mensajes.append(
                                error.get(
                                    "msg",
                                    "Error de validación"
                                )
                            )

                    if mensajes:
                        return " | ".join(mensajes)

                return str(detalle)

            if "mensaje" in datos:
                return str(datos["mensaje"])

        return str(datos)

    except Exception:
        return respuesta.text or "Ocurrió un error inesperado."


def headers_autenticacion():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def iniciar_sesion(email, password):
    try:
        respuesta = requests.post(
            f"{API_URL}/usuario/login",
            json={
                "email": email,
                "password": password
            },
            timeout=15
        )

        if respuesta.ok:
            datos = respuesta.json()

            st.session_state.token = datos.get("access_token")
            st.session_state.rol = datos.get("rol", "usuario")
            st.session_state.email = email

            return True, "Inicio de sesión correcto."

        return False, obtener_error(respuesta)

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con el servidor de NuevaMente."

    except requests.exceptions.Timeout:
        return False, "El servidor tardó demasiado en responder."

    except requests.exceptions.RequestException as error:
        return False, f"Error de conexión: {error}"


def registrar_usuario(email, password):
    try:
        respuesta = requests.post(
            f"{API_URL}/usuario/registro",
            json={
                "email": email,
                "password": password
            },
            timeout=15
        )

        if respuesta.ok:
            datos = respuesta.json()

            return True, datos.get(
                "mensaje",
                "Cuenta creada correctamente."
            )

        return False, obtener_error(respuesta)

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con el servidor de NuevaMente."

    except requests.exceptions.Timeout:
        return False, "El servidor tardó demasiado en responder."

    except requests.exceptions.RequestException as error:
        return False, f"Error de conexión: {error}"


def generar_document_id():
    return f"doc_{uuid.uuid4().hex[:12]}"


def cargar_documento(archivo, tenant_id):
    document_id = generar_document_id()

    try:
        archivos = {
            "file": (
                archivo.name,
                archivo.getvalue(),
                archivo.type or "application/octet-stream"
            )
        }

        datos = {
            "tenant_id": tenant_id,
            "document_id": document_id
        }

        respuesta = requests.post(
            f"{API_URL}/api/ingest",
            files=archivos,
            data=datos,
            headers=headers_autenticacion(),
            timeout=120
        )

        if respuesta.ok:
            resultado = respuesta.json()

            st.session_state.document_id = document_id

            st.session_state.documentos.append(
                {
                    "nombre": archivo.name,
                    "document_id": document_id,
                    "tenant_id": tenant_id
                }
            )

            return True, resultado

        return False, obtener_error(respuesta)

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con el servidor de NuevaMente."

    except requests.exceptions.Timeout:
        return False, "El procesamiento del documento tardó demasiado."

    except requests.exceptions.RequestException as error:
        return False, f"Error de conexión: {error}"


def consultar_rag(pregunta, tenant_id):
    try:
        datos = {
            "query": pregunta,
            "index_dir": "data/index",
            "top_k": 3,
            "tenant_id": tenant_id
        }

        respuesta = requests.post(
            f"{API_URL}/api/search",
            json=datos,
            headers=headers_autenticacion(),
            timeout=60
        )

        if respuesta.ok:
            return True, respuesta.json()

        return False, obtener_error(respuesta)

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con el servidor de NuevaMente."

    except requests.exceptions.Timeout:
        return False, "La consulta tardó demasiado."

    except requests.exceptions.RequestException as error:
        return False, f"Error de conexión: {error}"