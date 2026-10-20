
import json
import re
from pathlib import Path

import streamlit as st

from services.api import consultar_rag


# ============================================================
# CARGAR ESTILOS DE CONSULTA
# ============================================================

def cargar_estilos_consulta():
    ruta_css = (
        Path(__file__).resolve().parent.parent
        / "styles"
        / "consulta.css"
    )

    if ruta_css.exists():
        css = ruta_css.read_text(encoding="utf-8")

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )


# ============================================================
# LIMPIEZA Y NORMALIZACION DEL TEXTO
# ============================================================

def limpiar_texto(texto):
    """
    Limpia y normaliza el contenido recuperado del motor RAG.

    Conserva parrafos, listas, titulos, tablas y bloques de codigo.
    """

    if texto is None:
        return ""

    if not isinstance(texto, str):
        try:
            texto = json.dumps(texto, ensure_ascii=False)
        except (TypeError, ValueError):
            texto = str(texto)

    texto = texto.strip()

    if not texto:
        return ""

    # Extraer texto cuando el contenido sea JSON
    if texto.startswith("{") and texto.endswith("}"):
        try:
            datos = json.loads(texto)

            if isinstance(datos, dict):
                for clave in ("texto", "content", "page_content"):
                    if clave in datos:
                        texto = str(datos[clave] or "")
                        break

        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    # Eliminar envolturas simples
    texto = re.sub(
        r'^\s*"?texto"?\s*:\s*',
        "",
        texto,
        flags=re.IGNORECASE,
    ).strip()

    if len(texto) >= 2 and texto[0] == texto[-1] == '"':
        texto = texto[1:-1]

    # Normalizar saltos de linea
    texto = re.sub(r"\\+r\\+n", "\n", texto)
    texto = re.sub(r"\\+n", "\n", texto)
    texto = re.sub(r"\\+r(?![A-Za-z])", "\n", texto)

    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = texto.replace("\x00", "")

    # Normalizar espacios sin destruir el formato
    lineas = texto.split("\n")
    lineas_limpias = []

    for linea in lineas:
        linea = linea.replace("\t", " ")
        linea = re.sub(r" {2,}", " ", linea)
        linea = linea.strip()

        lineas_limpias.append(linea)

    texto = "\n".join(lineas_limpias)

    # Reducir saltos excesivos
    texto = re.sub(
        r"\n[ \t]*\n(?:[ \t]*\n)+",
        "\n\n",
        texto,
    )

    # Preservar estructuras Markdown
    lineas = texto.split("\n")
    resultado = []
    en_bloque_codigo = False

    patron_estructura = re.compile(
        r"^(?:"
        r"#{1,6}\s|"
        r"[-*+]\s|"
        r"\d+[.)]\s|"
        r">\s?|"
        r"\|.*\||"
        r"```|"
        r"~~~|"
        r"<(?:div|p|br|ul|ol|li)\b"
        r")",
        flags=re.IGNORECASE,
    )

    for linea in lineas:

        if linea.startswith(("```", "~~~")):
            en_bloque_codigo = not en_bloque_codigo
            resultado.append(linea)
            continue

        if en_bloque_codigo:
            resultado.append(linea)
            continue

        if not linea:
            if resultado and resultado[-1] != "":
                resultado.append("")
            continue

        es_estructura = bool(patron_estructura.match(linea))

        if not resultado or not resultado[-1]:
            resultado.append(linea)
            continue

        linea_anterior = resultado[-1]

        anterior_es_estructura = bool(
            patron_estructura.match(linea_anterior)
        )

        if es_estructura or anterior_es_estructura:
            resultado.append(linea)
        else:
            resultado[-1] = linea_anterior + " " + linea

    texto = "\n".join(resultado)

    # Corregir espacios antes de signos de puntuacion
    texto = re.sub(r"[ \t]+([,.;:!?])", r"\1", texto)

    return texto.strip()


# ============================================================
# MOSTRAR FRAGMENTOS RECUPERADOS
# ============================================================

def mostrar_fragmentos(resultados, tenant_id):

    for indice, resultado in enumerate(resultados, start=1):

        if not isinstance(resultado, dict):
            continue

        texto_original = resultado.get("page_content", "")
        texto = limpiar_texto(texto_original)

        metadata = resultado.get("metadata") or {}

        if not isinstance(metadata, dict):
            metadata = {}

        origen = metadata.get(
            "origen",
            "Documento sin nombre",
        )

        document_id = metadata.get(
            "document_id",
            "No disponible",
        )

        tenant_resultado = metadata.get(
            "tenant_id",
            tenant_id,
        )

        with st.container(border=True):

            st.markdown(f"#### Fragmento {indice}")

            if texto:
                st.markdown(texto)
            else:
                st.caption("Sin contenido disponible.")

            st.divider()

            st.caption(f"Documento: {origen}")

            with st.expander("Ver detalles del fragmento"):
                st.text(f"Document ID: {document_id}")
                st.text(
                    f"Espacio de consulta: {tenant_resultado}"
                )


# ============================================================
# INTERFAZ PRINCIPAL DE CONSULTA
# ============================================================

def mostrar_consulta():

    cargar_estilos_consulta()

    # Encabezado principal
    st.markdown(
        """
<div class="consulta-hero">
    <div class="consulta-etiqueta">
        CONSULTA INTELIGENTE
    </div>
    <h1>Consultar documento</h1>
    <p>
        Haz preguntas sobre tus documentos y descubre
        información relevante mediante inteligencia artificial.
    </p>
</div>
        """.strip(),
        unsafe_allow_html=True,
    )

    columna_formulario, columna_info = st.columns(
        [1.8, 1],
        gap="large",
    )

    # Formulario
    with columna_formulario:

        st.markdown("### Realiza una consulta")

        tenant_id = st.text_input(
            "Espacio de consulta",
            value=st.session_state.get(
                "tenant_id",
                "equipo12",
            ),
            key="consulta_tenant_oficial",
        )

        pregunta = st.text_area(
            "¿Qué quieres saber?",
            placeholder="Escribe tu pregunta sobre el documento...",
            height=130,
            key="consulta_pregunta_oficial",
        )

        consultar = st.button(
            "Consultar documento",
            use_container_width=True,
            type="primary",
            key="consulta_boton_oficial",
        )

    # Tarjeta informativa
    with columna_info:

        st.markdown(
            """
<div class="consulta-info">
    <h3>¿Cómo funciona?</h3>
    <p>
        Escribe una pregunta relacionada con tus documentos.
    </p>
    <p>
        NuevaMente buscará los fragmentos más relevantes
        y mostrará la información encontrada.
    </p>
    <p>
        También podrás consultar el documento de origen
        y los detalles de cada resultado.
    </p>
</div>
            """.strip(),
            unsafe_allow_html=True,
        )

    # Historial de consultas en la sesion actual
    if "consulta_historial" not in st.session_state:
        st.session_state["consulta_historial"] = []

    # Ejecutar consulta
    if consultar:

        if not pregunta.strip():
            st.warning("Escribe una pregunta para continuar.")

        elif not tenant_id.strip():
            st.warning("Ingresa un espacio de consulta.")

        else:

            with st.spinner(
                "Buscando información en los documentos..."
            ):
                exito, respuesta = consultar_rag(
                    pregunta.strip(),
                    tenant_id.strip(),
                )

            # Validar respuesta del servidor
            if not exito:

                st.error("No fue posible completar la consulta.")
                st.caption(str(respuesta))

            elif not isinstance(respuesta, dict):

                st.error(
                    "El servidor devolvió una respuesta inesperada."
                )

            else:

                resultados = respuesta.get("results", [])

                if not isinstance(resultados, list):

                    st.error(
                        "El formato de los resultados no es válido."
                    )

                elif not resultados:

                    st.info(
                        "No se encontraron fragmentos "
                        "relacionados con tu pregunta."
                    )

                else:

                    # Guardar la consulta real en el historial
                    st.session_state["consulta_historial"].append(
                        {
                            "pregunta": pregunta.strip(),
                            "tenant_id": tenant_id.strip(),
                            "resultados": resultados,
                            "respuesta": respuesta,
                        }
                    )

    # Mostrar historial visual
    historial = st.session_state["consulta_historial"]

    if historial:

        st.markdown(
            '<div class="consulta-seccion">'
            'Historial de consultas'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="consulta-subtitulo">'
            'Preguntas realizadas durante esta sesión.'
            '</div>',
            unsafe_allow_html=True,
        )

        for numero_consulta, consulta in enumerate(
            historial,
            start=1,
        ):

            # Pregunta del usuario
            with st.chat_message("user"):
                st.markdown(consulta["pregunta"])

            # Respuesta de NuevaMente
            with st.chat_message("assistant"):

                resultados = consulta["resultados"]

                st.success(
                    f"Se encontraron {len(resultados)} "
                    "fragmentos relacionados con tu pregunta."
                )

                mostrar_fragmentos(
                    resultados,
                    consulta["tenant_id"],
                )

                with st.expander(
                    "Ver respuesta completa del servidor "
                    f"(consulta {numero_consulta})"
                ):
                    st.json(consulta["respuesta"])

        # Limpiar historial
        if st.button(
            "Limpiar historial",
            key="consulta_limpiar_historial",
        ):
            st.session_state["consulta_historial"] = []
            st.rerun()

    else:

        st.info(
            "Todavía no hay consultas en esta sesión. "
            "Escribe una pregunta para comenzar."
        )
