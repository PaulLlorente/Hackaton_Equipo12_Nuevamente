
import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from services.api import adaptar_contenido


def aplicar_estilos():
    ruta_css = (
        Path(__file__).resolve().parent.parent
        / "styles"
        / "adaptacion.css"
    )

    if ruta_css.exists():
        css = ruta_css.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )


def mostrar_resumen(resultado):
    st.subheader("Resumen educativo")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiempo de estudio",
            f"{resultado.get('tiempo_estudio', 0)} min"
        )

    with col2:
        st.metric("Formato", "Resumen")

    with st.container(border=True):
        st.markdown("**Conceptos clave**")
        st.write(resultado.get("conceptos_clave", ""))

    st.markdown("### Contenido")

    contenido = resultado.get("contenido_adaptado", "")

    with st.container(border=True):
        for parrafo in contenido.split("\n\n"):
            if parrafo.strip():
                st.write(parrafo.strip())

    st.caption(
        resultado.get("evaluacion_calidad", "")
    )


def mostrar_flashcards(resultado):
    tarjetas = resultado.get("contenido_adaptado", [])

    if not tarjetas:
        st.info("No hay tarjetas disponibles.")
        return

    if "indice_flashcard" not in st.session_state:
        st.session_state.indice_flashcard = 0

    if "mostrar_respuesta_flashcard" not in st.session_state:
        st.session_state.mostrar_respuesta_flashcard = False

    indice = min(
        st.session_state.indice_flashcard,
        len(tarjetas) - 1
    )

    st.session_state.indice_flashcard = indice

    tarjeta = tarjetas[indice]

    st.markdown("""
    <div class="nm-card-header">
        <h3>Tarjetas de estudio</h3>
        <p>Aprende a tu ritmo, una tarjeta a la vez.</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress((indice + 1) / len(tarjetas))

    st.markdown(
        f'<div class="nm-progress">'
        f'Tarjeta {indice + 1} de {len(tarjetas)}'
        f'</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("####  Flashcard")

        st.markdown(
            f"### {tarjeta.get('pregunta', 'Sin pregunta')}"
        )

        st.divider()

        if st.session_state.mostrar_respuesta_flashcard:
            st.success(
                tarjeta.get(
                    "respuesta",
                    "Sin respuesta disponible."
                )
            )

            if st.button(
                "Ocultar respuesta",
                use_container_width=True,
                key="ocultar_flashcard"
            ):
                st.session_state.mostrar_respuesta_flashcard = False
                st.rerun()

        else:
            if st.button(
                "Mostrar respuesta",
                type="primary",
                use_container_width=True,
                key="mostrar_flashcard"
            ):
                st.session_state.mostrar_respuesta_flashcard = True
                st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "← Anterior",
            disabled=indice == 0,
            use_container_width=True,
            key="anterior_flashcard"
        ):
            st.session_state.indice_flashcard -= 1
            st.session_state.mostrar_respuesta_flashcard = False
            st.rerun()

    with col2:
        if st.button(
            "Siguiente →",
            disabled=indice == len(tarjetas) - 1,
            use_container_width=True,
            key="siguiente_flashcard"
        ):
            st.session_state.indice_flashcard += 1
            st.session_state.mostrar_respuesta_flashcard = False
            st.rerun()


def mostrar_quiz(resultado):
    preguntas = resultado.get("contenido_adaptado", [])

    if not preguntas:
        st.info("No hay preguntas disponibles.")
        return

    if "indice_quiz" not in st.session_state:
        st.session_state.indice_quiz = 0

    if "mostrar_respuesta_quiz" not in st.session_state:
        st.session_state.mostrar_respuesta_quiz = False

    indice = min(
        st.session_state.indice_quiz,
        len(preguntas) - 1
    )

    st.session_state.indice_quiz = indice

    pregunta = preguntas[indice]

    st.markdown("""
    <div class="nm-card-header">
        <h3>Cuestionario interactivo</h3>
        <p>Comprueba lo aprendido con preguntas abiertas.</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress((indice + 1) / len(preguntas))

    st.markdown(
        f'<div class="nm-progress">'
        f'Pregunta {indice + 1} de {len(preguntas)}'
        f'</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown(
            f"### {pregunta.get('pregunta', 'Sin pregunta')}"
        )

        st.write(
            pregunta.get("opciones", "")
        )

        st.divider()

        if st.session_state.mostrar_respuesta_quiz:
            st.markdown("**Respuesta de referencia**")

            st.success(
                pregunta.get(
                    "respuesta_correcta",
                    "Sin respuesta disponible."
                )
            )

            if st.button(
                "Ocultar respuesta",
                use_container_width=True,
                key="ocultar_quiz"
            ):
                st.session_state.mostrar_respuesta_quiz = False
                st.rerun()

        else:
            if st.button(
                "Consultar respuesta",
                type="primary",
                use_container_width=True,
                key="mostrar_quiz"
            ):
                st.session_state.mostrar_respuesta_quiz = True
                st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "← Anterior",
            disabled=indice == 0,
            use_container_width=True,
            key="anterior_quiz"
        ):
            st.session_state.indice_quiz -= 1
            st.session_state.mostrar_respuesta_quiz = False
            st.rerun()

    with col2:
        if indice == len(preguntas) - 1:
            if st.button(
                "Reiniciar quiz",
                use_container_width=True,
                key="reiniciar_quiz"
            ):
                st.session_state.indice_quiz = 0
                st.session_state.mostrar_respuesta_quiz = False
                st.rerun()
        else:
            if st.button(
                "Siguiente →",
                use_container_width=True,
                key="siguiente_quiz"
            ):
                st.session_state.indice_quiz += 1
                st.session_state.mostrar_respuesta_quiz = False
                st.rerun()


def mostrar_guion(resultado):
    st.subheader(
        resultado.get("titulo", "Guion educativo")
    )

    escenas = resultado.get("escenas", [])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Escenas", len(escenas))

    with col2:
        st.metric(
            "Duración estimada",
            resultado.get(
                "tiempo_estimado",
                "No especificada"
            )
        )

    st.markdown("### Desarrollo del guion")

    for escena in escenas:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"**Escena {escena.get('numero_escena', '')}**"
                )

            with col2:
                st.caption(
                    f"⏱ {escena.get('marca_tiempo', '')}"
                )

            st.write(
                escena.get(
                    "narrador",
                    "Sin narración disponible."
                )
            )


def mostrar_resultado(resultado):
    formato = resultado.get("formato", "")

    st.divider()
    st.markdown("## Material generado")

    if formato == "resumen":
        mostrar_resumen(resultado)

    elif formato == "flashcard":
        mostrar_flashcards(resultado)

    elif formato == "quiz":
        mostrar_quiz(resultado)

    elif formato == "guion":
        mostrar_guion(resultado)

    else:
        st.json(resultado)


def guardar_en_libreria(resultado, query, perfil, tenant_id):
    if "material_history" not in st.session_state:
        st.session_state.material_history = []

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "archivo": query,
        "perfil": perfil,
        "tenant_id": tenant_id,
        "formato": resultado.get("formato", "desconocido"),
        "resultado": resultado
    }

    st.session_state.material_history.insert(0, registro)


def mostrar_adaptacion():
    aplicar_estilos()

    st.markdown("""
    <div class="nm-hero">
        <h2>Adaptar contenido</h2>
        <p>
            Transforma documentos en materiales educativos
            interactivos y personalizados.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Configuración del material")

    with st.form("formulario_adaptacion"):
        query = st.text_area(
            "Tema o pregunta",
            placeholder=(
                "Ejemplo: ¿Qué es Oracle AI Success Navigator "
                "y para qué sirve?"
            ),
            height=110
        )

        tenant_id = st.text_input(
            "Espacio de trabajo",
            value=st.session_state.get(
                "tenant_id",
                "equipo12"
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            perfil = st.selectbox(
                "Perfil de aprendizaje",
                [
                    "principiante",
                    "intermedio",
                    "avanzado"
                ],
                index=1
            )

        with col2:
            formatos = {
                "Resumen": "resumen",
                "Flashcards": "flashcard",
                "Quiz": "quiz",
                "Guion": "guion"
            }

            formato_visible = st.selectbox(
                "Formato de salida",
                list(formatos.keys())
            )

        top_k = st.slider(
            "Fragmentos de contexto",
            min_value=1,
            max_value=10,
            value=3
        )

        enviar = st.form_submit_button(
            "Generar contenido",
            type="primary",
            use_container_width=True
        )

    if enviar:
        if not query.strip():
            st.warning("Escribe un tema o una pregunta.")
            return

        if not tenant_id.strip():
            st.warning("Ingresa un espacio de trabajo.")
            return

        st.session_state.tenant_id = tenant_id.strip()

        with st.spinner("Preparando material educativo..."):
            correcto, resultado = adaptar_contenido(
                query=query.strip(),
                tenant_id=tenant_id.strip(),
                perfil=perfil,
                formato=formatos[formato_visible],
                top_k=top_k
            )

        if correcto:
            if not isinstance(resultado, dict):
                st.error(
                    "El backend devolvió un resultado inesperado."
                )
                return

            st.session_state.resultado_adaptacion = resultado

            st.session_state.indice_flashcard = 0
            st.session_state.mostrar_respuesta_flashcard = False

            st.session_state.indice_quiz = 0
            st.session_state.mostrar_respuesta_quiz = False

            guardar_en_libreria(
                resultado=resultado,
                query=query.strip(),
                perfil=perfil,
                tenant_id=tenant_id.strip()
            )

            st.success(
                "Material generado correctamente "
                "y agregado a la Librería."
            )

        else:
            st.error(str(resultado))
            return

    resultado_guardado = st.session_state.get(
        "resultado_adaptacion"
    )

    if resultado_guardado:
        mostrar_resultado(resultado_guardado)

        st.download_button(
            "Descargar material en JSON",
            data=json.dumps(
                resultado_guardado,
                ensure_ascii=False,
                indent=2
            ),
            file_name="contenido_adaptado.json",
            mime="application/json",
            use_container_width=True
        )
