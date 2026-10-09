
import streamlit as st


def mostrar_inicio():
    st.markdown(
        """
        <div class="hero">
            <span class="status">● Plataforma NuevaMente</span>
            <h1>Aprende de otra manera.</h1>
            <p>
                Sube documentación técnica, consulta su contenido
                y genera materiales adaptados para facilitar el aprendizaje.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Panel de control")
    st.caption(
        "Resumen de la actividad y herramientas disponibles."
    )

    documentos = st.session_state.get("documentos", [])
    materiales = st.session_state.get("material_history", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Documentos de la sesión",
            value=len(documentos)
        )

    with col2:
        st.metric(
            label="Materiales generados",
            value=len(materiales)
        )

    with col3:
        st.metric(
            label="Formatos disponibles",
            value=4
        )

    st.divider()

    st.subheader("Herramientas de NuevaMente")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>Ingesta de documentos</h3>
                <p>
                    Procesa documentos PDF y Markdown para integrarlos
                    al flujo de conocimiento de NuevaMente.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Cargar documento",
            key="inicio_cargar",
            use_container_width=True
        ):
            st.session_state.pagina = "Cargar documento"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>Consulta inteligente</h3>
                <p>
                    Realiza preguntas sobre los documentos procesados
                    mediante el sistema RAG.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Consultar documento",
            key="inicio_consultar",
            use_container_width=True
        ):
            st.session_state.pagina = "Consultar documento"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>Contenido adaptado</h3>
                <p>
                    Convierte información técnica en resúmenes,
                    flashcards, cuestionarios y guiones.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Adaptar contenido",
            key="inicio_adaptar",
            use_container_width=True
        ):
            st.session_state.pagina = "Adaptar contenido"
            st.rerun()

    st.divider()

    col_actividad, col_espacio = st.columns([2, 1])

    with col_actividad:
        st.subheader("Actividad reciente")

        if materiales:
            for indice, material in enumerate(materiales[:5]):
                with st.container(border=True):
                    st.write(
                        f"**{material.get('archivo', 'Material educativo')}**"
                    )

                    st.caption(
                        f"{material.get('formato', 'Sin formato')} | "
                        f"{material.get('fecha', 'Sin fecha')}"
                    )

                    if st.button(
                        "Ver en Librería",
                        key=f"ver_material_{indice}"
                    ):
                        st.session_state.pagina = "Librería"
                        st.rerun()

        elif documentos:
            for indice, documento in enumerate(documentos[-5:]):
                with st.container(border=True):
                    if isinstance(documento, dict):
                        nombre = documento.get(
                            "nombre",
                            documento.get(
                                "nombre_archivo",
                                f"Documento {indice + 1}"
                            )
                        )
                    else:
                        nombre = str(documento)

                    st.write(f"**{nombre}**")
                    st.caption("Documento registrado en la sesión")

        else:
            st.info(
                "Todavía no hay actividad registrada en esta sesión."
            )

    with col_espacio:
        st.subheader("Espacio de trabajo")

        with st.container(border=True):
            st.write("**Tenant actual**")
            st.code(
                st.session_state.get("tenant_id", "equipo12"),
                language=None
            )

            st.write("**Último documento**")

            document_id = st.session_state.get("document_id")

            if document_id:
                st.code(document_id, language=None)
            else:
                st.caption(
                    "Todavía no hay un documento seleccionado."
                )

            st.write("**Estado de la sesión**")
            st.caption(
                "Modo demostración"
                if not st.session_state.get("token")
                else "Sesión con token disponible"
            )
