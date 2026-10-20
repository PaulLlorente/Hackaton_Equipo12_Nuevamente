
import html

import streamlit as st

from utils.metadata import formatear_document_id


def mostrar_inicio():
    documentos = st.session_state.get("documentos", [])
    materiales = st.session_state.get("material_history", [])

    st.markdown(
        """
        <section class="dashboard-hero">
            <div class="dashboard-hero-content">
                <span class="dashboard-eyebrow">
                    TU ESPACIO DE APRENDIZAJE
                </span>
                <h1>
                    <span style="color:#f1f5ff !important;">Aprende de</span>
                    <span style="color:#f44ec6 !important;">otra manera.</span>
                </h1>
                <p>
                    Transforma documentación técnica en experiencias
                    de aprendizaje inteligentes, claras y personalizadas.
                </p>
                <div class="dashboard-hero-tags">
                    <span>Documentos</span>
                    <span>Inteligencia artificial</span>
                    <span>Aprendizaje adaptativo</span>
                </div>
            </div>
            <div class="dashboard-hero-art" aria-hidden="true">
                <div class="dashboard-orbit">
                    <div class="dashboard-orbit-core">NM</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="dashboard-section-heading">
            <h2>Panel de control</h2>
            <p>Resumen de tu espacio de trabajo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    metricas = [
        ("▤", "Documentos", len(documentos), "Registrados en esta sesión", "cyan"),
        ("✦", "Materiales", len(materiales), "Contenidos generados", "pink"),
        ("▦", "Formatos", 5, "Opciones disponibles", "cyan")
    ]

    columnas = st.columns(3, gap="medium")

    for columna, (icono, titulo, valor, descripcion, color) in zip(
        columnas, metricas
    ):
        with columna:
            st.markdown(
                f"""
                <div class="dashboard-stat dashboard-stat-{color}">
                    <div class="dashboard-stat-top">
                        <span class="dashboard-stat-icon">{icono}</span>
                        <span class="dashboard-stat-label">{titulo}</span>
                    </div>
                    <div class="dashboard-stat-number">{valor}</div>
                    <div class="dashboard-stat-description">{descripcion}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="dashboard-section-heading dashboard-tools-heading">
            <h2>Herramientas principales</h2>
            <p>Todo lo que necesitas para comenzar.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    herramientas = [
        {
            "icono": "↑",
            "titulo": "Ingesta de documentos",
            "descripcion": "Sube y procesa archivos PDF y Markdown.",
            "etiqueta": "GESTIÓN DOCUMENTAL",
            "boton": "Cargar documento",
            "destino": "Cargar documento",
            "clave": "inicio_cargar",
            "color": "cyan"
        },
        {
            "icono": "✦",
            "titulo": "Contenido adaptado",
            "descripcion": "Genera resúmenes, flashcards, cuestionarios y guiones.",
            "etiqueta": "APRENDIZAJE CON IA",
            "boton": "Adaptar contenido",
            "destino": "Adaptar contenido",
            "clave": "inicio_adaptar",
            "color": "pink"
        },
        {
            "icono": "◎",
            "titulo": "Consulta inteligente",
            "descripcion": "Realiza preguntas sobre tus documentos mediante RAG.",
            "etiqueta": "BÚSQUEDA INTELIGENTE",
            "boton": "Consultar documento",
            "destino": "Consultar documento",
            "clave": "inicio_consultar",
            "color": "cyan"
        }
    ]

    columnas = st.columns(3, gap="medium")

    for columna, herramienta in zip(columnas, herramientas):
        with columna:
            with st.container(
                key=f"dashboard-tool-{herramienta['clave']}"
            ):
                st.markdown(
                    f"""
                    <div class="dashboard-tool-content">
                        <div class="dashboard-tool-icon dashboard-icon-{herramienta['color']}">
                            {herramienta['icono']}
                        </div>
                        <div class="dashboard-tool-tag">
                            {herramienta['etiqueta']}
                        </div>
                        <h3>{herramienta['titulo']}</h3>
                        <p>{herramienta['descripcion']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    herramienta["boton"],
                    key=herramienta["clave"],
                    use_container_width=True,
                    type=(
                        "primary"
                        if herramienta["color"] == "pink"
                        else "secondary"
                    )
                ):
                    st.session_state.ir_a = herramienta["destino"]
                    st.rerun()

    st.markdown(
        """
        <div class="dashboard-section-heading dashboard-bottom-heading">
            <h2>Tu actividad</h2>
            <p>Información reciente y estado del espacio de trabajo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_actividad, col_espacio = st.columns(
        [1.7, 1],
        gap="medium"
    )

    with col_actividad:
        with st.container(key="dashboard-activity"):
            st.markdown("#### Actividad reciente")

            if materiales:
                for indice, material in enumerate(materiales[:5]):
                    nombre = html.escape(
                        str(material.get("archivo", "Material educativo"))
                    )
                    formato = html.escape(
                        str(material.get("formato", "Sin formato"))
                    )
                    fecha = html.escape(
                        str(material.get("fecha", "Sin fecha"))
                    )

                    st.markdown(
                        f"""
                        <div class="dashboard-activity-item">
                            <span class="dashboard-activity-icon">✦</span>
                            <div>
                                <strong>{nombre}</strong>
                                <p>{formato} · {fecha}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Ver en Librería",
                        key=f"ver_material_{indice}"
                    ):
                        st.session_state.material_libreria_activo = (
                            material.get("resultado")
                        )
                        st.session_state.ir_a = "Librería"
                        st.session_state.mostrar_respuesta_flashcard = False
                        st.session_state.indice_quiz = 0
                        st.session_state.indice_flashcard = 0
                        st.rerun()

            elif documentos:
                for indice, documento in enumerate(documentos[-5:]):
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

                    nombre = html.escape(str(nombre))

                    st.markdown(
                        f"""
                        <div class="dashboard-activity-item">
                            <span class="dashboard-activity-icon">▤</span>
                            <div>
                                <strong>{nombre}</strong>
                                <p>Documento registrado en la sesión</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.markdown(
                    """
                    <div class="dashboard-empty">
                        <span>◇</span>
                        <strong>Aún no hay actividad</strong>
                        <p>Tus documentos y materiales aparecerán aquí.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with col_espacio:
        with st.container(key="dashboard-workspace"):
            st.markdown("#### Espacio de trabajo")

            tenant = html.escape(
                str(st.session_state.get("tenant_id", "equipo12"))
            )

            document_id = st.session_state.get("document_id")

            if document_id:
                ultimo_nombre = (
                    documentos[-1].get("nombre")
                    if documentos and isinstance(documentos[-1], dict)
                    else None
                )

                documento_actual = html.escape(
                    str(
                        formatear_document_id(
                            document_id,
                            ultimo_nombre
                        )
                    )
                )
            else:
                documento_actual = "Sin documento seleccionado"

            estado = (
                "Sesión con token disponible"
                if st.session_state.get("token")
                else "Modo demostración"
            )

            st.markdown(
                f"""
                <div class="dashboard-workspace-row">
                    <span>Tenant actual</span>
                    <strong>{tenant}</strong>
                </div>
                <div class="dashboard-workspace-row">
                    <span>Último documento</span>
                    <strong>{documento_actual}</strong>
                </div>
                <div class="dashboard-workspace-row">
                    <span>Estado de la sesión</span>
                    <strong>{estado}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="dashboard-footer">
            NuevaMente · Plataforma de aprendizaje inteligente
        </div>
        """,
        unsafe_allow_html=True
    )
