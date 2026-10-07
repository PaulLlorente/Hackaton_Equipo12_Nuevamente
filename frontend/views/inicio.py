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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>📄 Ingesta de documentos</h3>
                <p>
                    Procesa documentos PDF y Markdown para integrarlos
                    al flujo de conocimiento de NuevaMente.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>🔎 Consulta inteligente</h3>
                <p>
                    Realiza preguntas sobre los documentos procesados
                    mediante el sistema RAG.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>✨ Contenido adaptado</h3>
                <p>
                    Convierte información técnica en resúmenes,
                    flashcards, cuestionarios y guiones.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Tu espacio de trabajo")
    st.write(f"**Tenant actual:** `{st.session_state.tenant_id}`")

    if st.session_state.document_id:
        st.write(
            f"**Último documento:** "
            f"`{st.session_state.document_id}`"
        )
    else:
        st.caption(
            "Todavía no has procesado documentos en esta sesión."
        )