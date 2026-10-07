import streamlit as st

from services.api import cargar_documento


def mostrar_carga():
    st.title("📄 Cargar documento")

    st.write(
        "Sube un documento para incorporarlo al sistema de NuevaMente."
    )

    st.info("Formatos disponibles actualmente: PDF y Markdown.")

    tenant_id = st.text_input(
        "Identificador del espacio",
        value=st.session_state.tenant_id,
        help="Identifica el espacio al que pertenecerán los documentos."
    )

    archivo = st.file_uploader(
        "Selecciona un documento",
        type=["pdf", "md"]
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
        use_container_width=True
    ):
        tenant_id = tenant_id.strip()

        if not tenant_id:
            st.warning(
                "Ingresa un identificador para tu espacio."
            )

        elif archivo is None:
            st.warning(
                "Selecciona un archivo PDF o Markdown."
            )

        else:
            st.session_state.tenant_id = tenant_id

            with st.spinner("Procesando documento..."):
                correcto, resultado = cargar_documento(
                    archivo,
                    tenant_id
                )

            if correcto:
                st.success(
                    "Documento procesado correctamente."
                )

                document_id = resultado.get(
                    "document_id",
                    st.session_state.document_id
                )

                st.write(
                    f"**Document ID:** `{document_id}`"
                )

                if resultado.get("mensaje"):
                    st.info(resultado["mensaje"])

                with st.expander("Ver respuesta del servidor"):
                    st.json(resultado)

            else:
                st.error(resultado)

    if st.session_state.documentos:
        st.divider()
        st.subheader("Documentos de esta sesión")

        for documento in reversed(
            st.session_state.documentos
        ):
            st.markdown(
                f"""
                **📄 {documento["nombre"]}**

                Document ID: `{documento["document_id"]}`  
                Tenant: `{documento["tenant_id"]}`
                """
            )