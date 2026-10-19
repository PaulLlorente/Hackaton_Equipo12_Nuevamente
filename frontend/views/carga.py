import streamlit as st

from services.api import cargar_documento
from utils.metadata import formatear_document_id


def mostrar_carga():
    st.title("Cargar documento")

    st.write(
        "Sube un documento para incorporarlo al sistema de NuevaMente."
    )

    st.info("Formatos disponibles actualmente: PDF y Markdown.")

    tenant_id = st.text_input(
        "Identificador del espacio",
        value=st.session_state.get("tenant_id", "equipo12"),
        help="Identifica el espacio al que pertenecerán los documentos."
    )

    archivo = st.file_uploader(
        "Selecciona un documento",
        type=["pdf", "md"], 
        max_upload_size = 10 
    )

    if archivo is not None:
        st.write(f"**Archivo:** {archivo.name}")
        st.write(f"**Tamaño:** {archivo.size / 1024:.2f} KB")

        extension = archivo.name.lower().split(".")[-1]

        if extension == "pdf":
            st.caption("Tipo detectado: Documento PDF")

        elif extension == "md":
            st.caption("Tipo detectado: Documento Markdown")

    if st.button(
        "Procesar documento",
        type="primary",
        use_container_width=True,
        key="procesar_doc"
    ):
        tenant_id = tenant_id.strip()

        if not tenant_id:
            st.warning(
                "Ingresa un identificador para tu espacio."
            )
            return

        if archivo is None:
            st.warning(
                "Selecciona un archivo PDF o Markdown."
            )
            return

        st.session_state.tenant_id = tenant_id

        with st.spinner("Procesando documento..."):
            try:
                correcto, resultado = cargar_documento(
                    archivo,
                    tenant_id
                )
            except Exception as error:
                st.error(
                    f"No se pudo completar la solicitud: {error}"
                )
                return

        if correcto:
            if not isinstance(resultado, dict):
                st.error(
                    "El servidor devolvió una respuesta inesperada."
                )
                return

            raw_doc_id = resultado.get("document_id")
            document_id = (
                formatear_document_id(raw_doc_id, archivo.name)
                if raw_doc_id
                else None
            )

            if document_id:
                st.session_state.document_id = document_id

            if "documentos" not in st.session_state:
                st.session_state.documentos = []

            registro = {
                "nombre": archivo.name,
                "document_id": document_id,
                "tenant_id": tenant_id
            }

            existe = any(
                documento.get("document_id") == document_id
                and documento.get("tenant_id") == tenant_id
                for documento in st.session_state.documentos
            ) if document_id else False

            if not existe:
                st.session_state.documentos.append(registro)

            st.success(
                "¡Documento procesado con éxito! Ya puedes adaptar su contenido a tu nivel de aprendizaje."
            )

            if document_id:
                st.write(f"**Document ID:** `{document_id}`")
            else:
                st.caption(
                    "La respuesta no incluyó un identificador de documento."
                )

            if resultado.get("mensaje"):
                st.info(resultado["mensaje"])

            with st.expander("Ver respuesta del servidor"):
                st.json(resultado)

        else:
            st.error(str(resultado))

    documentos = st.session_state.get("documentos", [])

    if documentos:
        st.divider()
        st.subheader("Documentos de esta sesión")

        for documento in reversed(documentos):
            with st.container(border=True):
                nombre_doc = documento.get("nombre", "Documento")
                doc_id_legible = formatear_document_id(
                    documento.get("document_id"), nombre_doc
                )
                st.write(f"**{nombre_doc}**")
                st.write(f"Document ID: `{doc_id_legible}`")
                st.write(f"Tenant: `{documento.get('tenant_id', '')}`")
