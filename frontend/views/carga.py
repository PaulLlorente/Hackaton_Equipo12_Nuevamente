import html

import streamlit as st

from services.api import cargar_documento
from utils.metadata import formatear_document_id


def mostrar_carga():
    st.markdown(
        """
        <section class="carga-hero">
            <div class="carga-eyebrow">GESTIÓN DOCUMENTAL</div>
            <h1>
                <span style="color:#f1f5ff !important;">Cargar</span>
                <span style="color:#f44ec6 !important;">documento</span>
            </h1>
            <p>
                Incorpora documentos técnicos a tu espacio de conocimiento
                para consultarlos y generar materiales educativos.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col_formulario, col_informacion = st.columns([1.15, 1], gap="large")

    with col_formulario:
        with st.container(key="carga-formulario"):
            st.markdown("### Subir archivo")
            st.caption("Selecciona el espacio de trabajo y el documento.")

            tenant_id = st.text_input(
                "Identificador del espacio",
                value=st.session_state.get("tenant_id", "equipo12"),
                help="Identifica el espacio al que pertenecerán los documentos.",
                key="carga_tenant",
            )

            archivo = st.file_uploader(
                "Selecciona un documento",
                type=["pdf", "md"],
                max_upload_size=10,
                key="carga_archivo",
            )

            st.caption("Formatos admitidos: PDF y Markdown. Máximo 10 MB.")

            procesar = st.button(
                "Procesar documento",
                type="primary",
                use_container_width=True,
                key="procesar_doc",
            )

    with col_informacion:
        with st.container(key="carga-informacion"):
            st.markdown("### Información del documento")

            if archivo is not None:
                nombre = html.escape(archivo.name)
                tamano = archivo.size / 1024
                extension = archivo.name.lower().rsplit(".", 1)[-1]

                tipo = "Documento PDF" if extension == "pdf" else "Documento Markdown"

                st.markdown(
                    f"""
                    <div class="carga-file-info">
                        <div class="carga-file-icon">▤</div>
                        <div class="carga-file-name">{nombre}</div>
                        <div class="carga-file-type">{tipo}</div>
                    </div>
                    <div class="carga-detail-row">
                        <span>Tamaño</span>
                        <strong>{tamano:.2f} KB</strong>
                    </div>
                    <div class="carga-detail-row">
                        <span>Formato</span>
                        <strong>{extension.upper()}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:
                st.markdown(
                    """
                    <div class="carga-empty">
                        <div class="carga-empty-icon">▤</div>
                        <strong>Ningún archivo seleccionado</strong>
                        <p>
                            Aquí aparecerán el nombre, tamaño y formato
                            del documento que selecciones.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if procesar:
        tenant_id = tenant_id.strip()

        if not tenant_id:
            st.warning("Ingresa un identificador para tu espacio.")
            return

        if archivo is None:
            st.warning("Selecciona un archivo PDF o Markdown.")
            return

        st.session_state.tenant_id = tenant_id

        with st.spinner("Procesando documento..."):
            try:
                correcto, resultado = cargar_documento(archivo, tenant_id)
            except Exception as error:
                st.error(f"No se pudo completar la solicitud: {error}")
                return

        if correcto:
            if not isinstance(resultado, dict):
                st.error("El servidor devolvió una respuesta inesperada.")
                return

            raw_doc_id = resultado.get("document_id")
            document_id = (
                formatear_document_id(raw_doc_id, archivo.name) if raw_doc_id else None
            )

            if document_id:
                st.session_state.document_id = document_id

            if "documentos" not in st.session_state:
                st.session_state.documentos = []

            registro = {
                "nombre": archivo.name,
                "document_id": document_id,
                "tenant_id": tenant_id,
            }

            existe = (
                any(
                    documento.get("document_id") == document_id
                    and documento.get("tenant_id") == tenant_id
                    for documento in st.session_state.documentos
                )
                if document_id
                else False
            )

            if not existe:
                st.session_state.documentos.append(registro)

            es_duplicado = (
                existe or str(resultado.get("status", "")).lower() == "duplicate"
            )

            if es_duplicado:
                st.info(
                    f"✨ El documento **{archivo.name}** ya se encontraba "
                    "en tu espacio de estudio y está listo para usarse."
                )
            else:
                st.success(
                    f"✅ ¡Listo! **{archivo.name}** se procesó e incorporó "
                    "correctamente a tu espacio de estudio."
                )

            detalles_proceso = []
            if document_id:
                detalles_proceso.append(f"📄 **Referencia:** `{document_id}`")
            if tenant_id:
                detalles_proceso.append(f"🏢 **Espacio:** `{tenant_id}`")
            fragmentos = resultado.get("chunks_ingested")
            if isinstance(fragmentos, int) and fragmentos > 0:
                detalles_proceso.append(f"🧩 **Secciones indexadas:** `{fragmentos}`")

            if detalles_proceso:
                st.caption(" · ".join(detalles_proceso))

        else:
            texto_error = str(resultado)
            error_lower = texto_error.lower()

            # Interceptar error de cuota / saturación de Gemini (429)
            if (
                "429" in error_lower
                or "resource_exhausted" in error_lower
                or "quota" in error_lower
                or "rate limit" in error_lower
            ):
                st.warning(
                    "⏳ **Límite de servicio excedido temporalmente.**\n\n"
                    "La cuota de procesamiento de la IA ha alcanzado su límite por minuto. "
                    "Por favor, espera unos 30 a 60 segundos e intenta procesar el documento nuevamente."
                )
            else:
                st.error(f"No fue posible procesar el documento: {texto_error}")

    documentos = st.session_state.get("documentos", [])

    st.markdown(
        """
        <div class="carga-section-heading">
            <h2>Documentos de esta sesión</h2>
            <p>Consulta los documentos registrados en tu espacio de trabajo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if documentos:
        for documento in reversed(documentos):
            nombre_doc = str(documento.get("nombre", "Documento"))

            doc_id_legible = formatear_document_id(
                documento.get("document_id"), nombre_doc
            )

            nombre = html.escape(nombre_doc)
            identificador = html.escape(str(doc_id_legible or "No disponible"))
            tenant = html.escape(str(documento.get("tenant_id", "")))

            st.markdown(
                f"""
                <div class="carga-document-card">
                    <div class="carga-document-icon">▤</div>
                    <div class="carga-document-content">
                        <strong>{nombre}</strong>
                        <p>Document ID: {identificador}</p>
                        <span>Espacio: {tenant}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.markdown(
            """
            <div class="carga-history-empty">
                Aún no hay documentos registrados en esta sesión.
            </div>
            """,
            unsafe_allow_html=True,
        )
