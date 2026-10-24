from pathlib import Path

import streamlit as st

from services.api import consultar_rag
from utils.limpiar_texto import limpiar_texto
from utils.metadata import obtener_metadata


def cargar_estilos_consulta():
    ruta_css = Path(__file__).resolve().parent.parent / "styles" / "consulta.css"
    if ruta_css.exists():
        css = ruta_css.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def mostrar_fragmentos(resultados, tenant_id):
    for indice, resultado in enumerate(resultados, start=1):
        if not isinstance(resultado, dict):
            continue

        texto_original = resultado.get("page_content", "")
        texto = limpiar_texto(texto_original)
        origen, document_id, tenant_resultado = obtener_metadata(resultado, tenant_id)

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
                st.text(f"Espacio de consulta: {tenant_resultado}")


def mostrar_consulta():
    cargar_estilos_consulta()

    st.markdown(
        """
        <div class="consulta-hero">
            <div class="consulta-etiqueta">CONSULTA INTELIGENTE</div>
            <h1>Consultar documento</h1>
            <p>
                Haz preguntas sobre tus documentos y descubre
                información relevante mediante inteligencia artificial.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columna_formulario, columna_info = st.columns([1.8, 1], gap="large")

    with columna_formulario:
        st.markdown("### Realiza una consulta")

        tenant_id = st.text_input(
            "Espacio de consulta",
            value=st.session_state.get("tenant_id", "equipo12"),
            key="consulta_tenant_oficial",
        )

        top_k = st.slider(
            "Fragmentos a recuperar (RAG)",
            min_value=1,
            max_value=10,
            value=3,
            help=(
                "Define cuántos fragmentos recuperados se utilizarán como "
                "contexto para generar la respuesta."
            ),
            key="consulta_top_k_oficial",
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

    with columna_info:
        st.markdown(
            """
            <div class="consulta-info">
                <h3>¿Cómo funciona?</h3>
                <p>Escribe una pregunta relacionada con tus documentos.</p>
                <p>
                    NuevaMente buscará los fragmentos más relevantes
                    y mostrará la información encontrada.
                </p>
                <p>
                    También podrás consultar el documento de origen
                    y los detalles de cada resultado.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if "consulta_historial" not in st.session_state:
        st.session_state["consulta_historial"] = []

    if consultar:
        if not pregunta.strip():
            st.warning("Escribe una pregunta para continuar.")

        elif not tenant_id.strip():
            st.warning("Ingresa un espacio de consulta.")

        else:
            st.session_state.tenant_id = tenant_id.strip()

            with st.spinner("Buscando información en los documentos..."):
                exito, respuesta = consultar_rag(
                    pregunta.strip(),
                    tenant_id.strip(),
                    top_k=top_k,
                )

            if not exito:
                texto_error = str(respuesta)
                error_lower = texto_error.lower()

                if (
                    "429" in error_lower
                    or "resource_exhausted" in error_lower
                    or "quota" in error_lower
                    or "rate limit" in error_lower
                ):
                    st.warning(
                        "⏳ **Límite de servicio excedido temporalmente.**\n\n"
                        "La cuota de procesamiento de la IA ha alcanzado su límite por minuto. "
                        "Por favor, espera unos segundos e intenta realizar la consulta nuevamente."
                    )
                else:
                    st.error("No fue posible completar la consulta en este momento.")
                    st.caption(texto_error)

            elif not isinstance(respuesta, dict):
                st.warning(
                    "No pudimos interpretar la respuesta. Por favor, intenta de nuevo."
                )

            else:
                resultados = respuesta.get("results", [])

                if not isinstance(resultados, list):
                    st.warning(
                        "No fue posible recuperar los fragmentos de estudio en este intento."
                    )

                elif not resultados:
                    st.info(
                        "No se encontraron fragmentos relacionados con tu pregunta."
                    )

                else:
                    st.session_state["consulta_historial"].append(
                        {
                            "pregunta": pregunta.strip(),
                            "tenant_id": tenant_id.strip(),
                            "resultados": resultados,
                            "respuesta": respuesta,
                        }
                    )

    historial = st.session_state["consulta_historial"]

    if historial:
        st.markdown(
            '<div class="consulta-seccion">Historial de consultas</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="consulta-subtitulo">'
            "Preguntas realizadas durante esta sesión."
            "</div>",
            unsafe_allow_html=True,
        )

        for numero_consulta, consulta in enumerate(historial, start=1):
            with st.chat_message("user"):
                st.markdown(consulta["pregunta"])

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
