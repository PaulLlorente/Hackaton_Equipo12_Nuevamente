import streamlit as st

from utils.limpiar_texto import limpiar_texto
from utils.metadata import obtener_metadata
from services.api import consultar_rag

# ============================================================
# PRESENTACIÓN DE LA CONSULTA
# ============================================================


def mostrar_consulta():
    """Interfaz de Streamlit para consultar documentos mediante RAG."""

    st.title("Consultar documento")

    st.write("Haz una pregunta sobre la información que ha sido procesada.")

    # --------------------------------------------------------
    # 1. Datos de la consulta
    # --------------------------------------------------------
    col_tenant, col_topk = st.columns([2, 1])

    with col_tenant:
        tenant_id = st.text_input(
            "Espacio de consulta", value=st.session_state.get("tenant_id", "equipo12")
        )

    with col_topk:
        top_k = st.slider(
            "Fragmentos a recuperar (RAG)",
            min_value=1,
            max_value=10,
            value=3,
            help="Define cuántos fragmentos de texto recuperados se utilizarán como contexto para generar la respuesta. Un valor mayor aporta más contexto, pero puede incluir información menos relevante."
        )

    pregunta = st.text_area(
        "¿Qué quieres saber?",
        placeholder="Escribe tu pregunta sobre el documento...",
        height=100,
    )

    # --------------------------------------------------------
    # 2. Ejecutar consulta
    # --------------------------------------------------------
    if st.button("Consultar", type="primary", use_container_width=True):
        if not pregunta.strip():
            st.warning("Escribe una pregunta para continuar.")
            return

        if not tenant_id.strip():
            st.warning("Ingresa un espacio de consulta.")
            return

        st.session_state.tenant_id = tenant_id.strip()

        with st.spinner("Buscando información en los documentos..."):
            exito, respuesta = consultar_rag(
                pregunta.strip(), tenant_id.strip(), top_k=top_k
            )

        if not exito:
            st.error("No fue posible completar la consulta.")
            st.caption(str(respuesta))
            return

        if not isinstance(respuesta, dict):
            st.error("El servidor devolvió una respuesta inesperada.")
            return

        st.session_state.resultado_consulta = respuesta

    respuesta = st.session_state.get("resultado_consulta")
    if not respuesta:
        return

    resultados = respuesta.get("results", [])

    if not isinstance(resultados, list):
        st.error("El formato de los resultados no es válido.")
        return

    if not resultados:
        st.info("No se encontraron fragmentos relacionados con tu pregunta.")
        return

    # --------------------------------------------------------
    # 4. Resumen de resultados
    # --------------------------------------------------------
    st.success(
        f"Consulta realizada correctamente. "
        f"Se encontraron {len(resultados)} fragmentos."
    )

    st.subheader("Información encontrada")

    # --------------------------------------------------------
    # 5. Mostrar cada fragmento
    # --------------------------------------------------------
    for indice, resultado in enumerate(resultados, start=1):

        # Validar la estructura de cada resultado.
        if not isinstance(resultado, dict):
            continue

        # Limpiar el contenido textual.
        texto_original = resultado.get("page_content", "")
        texto = limpiar_texto(texto_original)

        origen, document_id, tenant_resultado = obtener_metadata(resultado, tenant_id)

        # ----------------------------------------------------
        # Tarjeta del fragmento
        # ----------------------------------------------------
        with st.container(border=True):

            st.markdown(f"### Fragmento {indice}")

            if texto:
                # Streamlit renderiza listas, títulos y párrafos
                # Markdown presentes en el contenido.
                st.markdown(texto)
            else:
                st.caption("Sin contenido disponible.")

            st.divider()

            st.caption(f"📄 Documento: {origen}")

            with st.expander("Ver detalles"):
                st.text(f"Document ID: {document_id}")
                st.text(f"Espacio de consulta: {tenant_resultado}")

    # --------------------------------------------------------
    # 6. Respuesta original de la API para depuración
    # --------------------------------------------------------
    with st.expander("Ver respuesta completa del servidor"):
        st.json(respuesta)
