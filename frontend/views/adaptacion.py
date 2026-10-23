import html
import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from utils.quiz import formatear_opciones
from services.api import adaptar_contenido
from utils.metadata import obtener_metadata


def aplicar_estilos():
    ruta_css = Path(__file__).resolve().parent.parent / "styles" / "adaptacion.css"

    if ruta_css.exists():
        css = ruta_css.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def mostrar_resumen(resultado):
    st.subheader("Resumen educativo")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Tiempo de estudio", f"{resultado.get('tiempo_estudio', 0)} min")

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

    st.caption(resultado.get("evaluacion_calidad", ""))


def _mostrar_respuesta_fc():
    st.session_state.mostrar_respuesta_flashcard = True


def _ocultar_respuesta_fc():
    st.session_state.mostrar_respuesta_flashcard = False


def _anterior_fc():
    st.session_state.indice_flashcard = max(
        0, st.session_state.get("indice_flashcard", 0) - 1
    )
    st.session_state.mostrar_respuesta_flashcard = False


def _siguiente_fc(total: int):
    st.session_state.indice_flashcard = min(
        total - 1, st.session_state.get("indice_flashcard", 0) + 1
    )
    st.session_state.mostrar_respuesta_flashcard = False


def _anterior_quiz():
    st.session_state.indice_quiz = max(0, st.session_state.get("indice_quiz", 0) - 1)


def _siguiente_quiz(total: int):
    st.session_state.indice_quiz = min(
        total - 1, st.session_state.get("indice_quiz", 0) + 1
    )


def _reiniciar_quiz():
    st.session_state.indice_quiz = 0


def _reiniciar_flashcards():
    st.session_state.indice_flashcard = 0
    st.session_state.mostrar_respuesta_flashcard = False


def mostrar_flashcards(resultado):
    tarjetas = resultado.get("contenido_adaptado", [])

    if not tarjetas:
        st.info("No hay tarjetas disponibles.")
        return

    if "indice_flashcard" not in st.session_state:
        st.session_state.indice_flashcard = 0

    if "mostrar_respuesta_flashcard" not in st.session_state:
        st.session_state.mostrar_respuesta_flashcard = False

    indice = min(st.session_state.indice_flashcard, len(tarjetas) - 1)

    st.session_state.indice_flashcard = indice

    tarjeta = tarjetas[indice]

    st.markdown(
        """
    <div class="nm-card-header">
        <h3>Tarjetas de estudio</h3>
        <p>Aprende a tu ritmo, una tarjeta a la vez.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("⏱️ Tiempo de estudio", f"{resultado.get('tiempo_estudio', 0)} min")
    with col_m2:
        st.metric("🗂️ Total de tarjetas", len(tarjetas))

    conceptos = (resultado.get("conceptos_clave") or "").strip()
    if conceptos:
        with st.expander("🔑 Conceptos clave", expanded=True):
            st.write(conceptos)

    st.progress((indice + 1) / len(tarjetas))

    st.markdown(
        f'<div class="nm-progress">'
        f"Tarjeta {indice + 1} de {len(tarjetas)}"
        f"</div>",
        unsafe_allow_html=True,
    )

    with st.container(border=False):
        mostrar = st.session_state.mostrar_respuesta_flashcard
        clase_giro = "is-flipped" if mostrar else ""
        pregunta_segura = html.escape(
            str(tarjeta.get("pregunta", "Sin pregunta"))
        )
        respuesta_segura = html.escape(
            str(tarjeta.get("respuesta", "Sin respuesta disponible."))
        )

        st.markdown(
            f"""
                <h3 class="nm-title-card"> FlashCard </h3>
            <label class="nm-flip-card" data-card="{indice}">
            <input type="checkbox" class="nm-flip-toggle" style="display:none">
                <div class="nm-flip-inner {clase_giro} ">
                    <div class="nm-flip-front"  >
                        <p>{pregunta_segura}</p>
                    </div>
                    <div class="nm-flip-back">
                        <p>{respuesta_segura}</p>
                    </div>
                </div>
            </label>
                    """,
            unsafe_allow_html=True,
        )

        if st.session_state.mostrar_respuesta_flashcard:
            st.button(
                "Ocultar respuesta",
                use_container_width=True,
                key="ocultar_flashcard",
                on_click=_ocultar_respuesta_fc,
            )
        else:
            st.button(
                "Mostrar respuesta",
                type="primary",
                use_container_width=True,
                key="mostrar_flashcard",
                on_click=_mostrar_respuesta_fc,
            )

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "← Anterior",
            disabled=indice == 0,
            use_container_width=True,
            key="anterior_flashcard",
            on_click=_anterior_fc,
        )

    with col2:
        if indice == len(tarjetas) - 1:
            st.button(
                "Reiniciar Flashcards ",
                use_container_width=True,
                key="flashcard_quiz",
                on_click=_reiniciar_flashcards,
            )
        else:
            st.button(
                "Siguiente →",
                disabled=indice == len(tarjetas) - 1,
                use_container_width=True,
                key="siguiente_flashcard",
                on_click=_siguiente_fc,
                args=(len(tarjetas),),
            )

    evaluacion = (resultado.get("evaluacion_calidad") or "").strip()
    if evaluacion:
        st.divider()
        st.caption(f"✨ **Evaluación de calidad:** {evaluacion}")


def mostrar_quiz(resultado):
    preguntas = resultado.get("contenido_adaptado", [])

    if not preguntas:
        st.info("No hay preguntas disponibles.")
        return

    if "indice_quiz" not in st.session_state:
        st.session_state.indice_quiz = 0

    indice = min(st.session_state.indice_quiz, len(preguntas) - 1)

    st.session_state.indice_quiz = indice

    pregunta = preguntas[indice]

    st.markdown(
        """
    <div class="nm-card-header">
        <h3>Cuestionario interactivo</h3>
        <p>Comprueba lo aprendido con preguntas de selección múltiple.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("⏱️ Tiempo de estudio", f"{resultado.get('tiempo_estudio', 0)} min")
    with col_m2:
        st.metric("❓ Total de preguntas", len(preguntas))

    conceptos = (resultado.get("conceptos_clave") or "").strip()
    if conceptos:
        with st.expander("🔑 Conceptos clave", expanded=True):
            st.write(conceptos)

    st.progress((indice + 1) / len(preguntas))

    st.markdown(
        f'<div class="nm-progress">'
        f"Pregunta {indice + 1} de {len(preguntas)}"
        f"</div>",
        unsafe_allow_html=True,
    )

    with st.container(border=False):
        st.markdown(f"### {pregunta.get('pregunta', 'Sin pregunta')}")

        opciones_lista = formatear_opciones(pregunta.get("opciones", ""))
        eleccion: str = st.radio(
            "Selecciona tu respuesta:",
            opciones_lista,
            key=f"quiz_option_{indice}",
            index=None,
        )

        st.divider()

        if st.button(
            "Consultar respuesta",
            type="primary",
            use_container_width=True,
            key=f"comprobar_{indice}",
        ):
            if not eleccion:
                st.warning("Por favor, selecciona una respuesta antes de consultarla.")
            else:
                respuesta_correcta = str(
                    pregunta.get(
                        "respuesta_correcta", "Sin respuesta disponible."
                    )
                ).strip()
                es_correcta = bool(respuesta_correcta) and (
                    respuesta_correcta.lower() in eleccion.lower()
                    or eleccion[0].upper() == respuesta_correcta[0].upper()
                )
                if es_correcta:
                    st.success("🎉 ¡Excelente! Respuesta correcta.")
                else:
                    st.error(
                        f"❌ Incorrecto. La respuesta correcta era: {respuesta_correcta}"
                    )

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "← Anterior",
            disabled=indice == 0,
            use_container_width=True,
            key="anterior_quiz",
            on_click=_anterior_quiz,
        )

    with col2:
        if indice == len(preguntas) - 1:
            st.button(
                "Reiniciar quiz",
                use_container_width=True,
                key="reiniciar_quiz",
                on_click=_reiniciar_quiz,
            )
        else:
            st.button(
                "Siguiente →",
                use_container_width=True,
                key="siguiente_quiz",
                on_click=_siguiente_quiz,
                args=(len(preguntas),),
            )

    evaluacion = (resultado.get("evaluacion_calidad") or "").strip()
    if evaluacion:
        st.divider()
        st.caption(f"✨ **Evaluación de calidad:** {evaluacion}")


def mostrar_guion(resultado):
    st.subheader(f"🎬 {resultado.get('titulo', 'Guion educativo')}")

    escenas = resultado.get("escenas", [])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎞️ Total de Escenas", len(escenas))

    with col2:
        st.metric(
            "⏱️ Duración estimada", resultado.get("tiempo_estimado", "No especificada")
        )

    st.divider()
    st.markdown("### 📜 Desarrollo del guion")

    for escena in escenas:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"#### Escena {escena.get('numero_escena', '')}")

            with col2:
                marca_segura = html.escape(
                    str(escena.get("marca_tiempo", ""))
                )
                st.markdown(
                    f"<div style='text-align: right; color: #64748b; font-weight: bold;'>⏱ {marca_segura}</div>",
                    unsafe_allow_html=True,
                )

            st.info(escena.get("narrador", "Sin narración disponible."), icon="🗣️")


def mostrar_tutorial(resultado: dict):

    st.markdown("## Tutorial de aprendizaje")
    st.subheader(f" {resultado.get('titulo', '')}", icon="📚")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        col1.metric(
            "⏰Tiempo estimado de aprendizaje",
            resultado.get("tiempo_estimado", "No especificado"),
        )
    with col2:
        col2.metric("Total de pasos", len(resultado.get("pasos", [])))

    requisitos = [r for r in resultado.get("requisitos_previos", [])]
    if requisitos:
        with st.expander("📋 Requisitos previos", expanded=True):
            for i, r in enumerate(requisitos):
                st.write(f"{i+1}. {r}")

    st.divider()
    st.markdown("## 📚 Paso a paso")

    for p in resultado.get("pasos", []):
        with st.container(border=True):
            st.markdown(f"### Paso {p['numero_paso']}: {p['titulo']}")

            st.write(p["instrucciones"])

            if (p.get("codigo_o_comando") or "").strip():
                st.code(p["codigo_o_comando"], language="bash")

            if (p.get("consejo_o_nota") or "").strip():
                st.info(p["consejo_o_nota"], icon="💡")


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

    elif formato == "tutorial":
        mostrar_tutorial(resultado)

    else:
        st.info(
            "El material se generó correctamente, pero su vista previa interactiva "
            "no está disponible para este formato. Puedes descargarlo a continuación."
        )
    fuentes = resultado.get("fuentes", [])
    if fuentes:
        st.divider()
        st.markdown("### 📚 Fuentes utilizadas")
        for fuente in fuentes:
            # Nota: obtener_metadata espera un dict con {"metadata": {...}}
            origen, doc_id, tenant_res = obtener_metadata(
                {"metadata": fuente},
                st.session_state.get("tenant_id", "equipo12"),
            )

            st.caption(f"📄 **{origen}** — ID: `{doc_id}` (Espacio: `{tenant_res}`)")


def guardar_en_libreria(resultado, query, perfil, tenant_id):
    if "material_history" not in st.session_state:
        st.session_state.material_history = []

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "archivo": query,
        "perfil": perfil,
        "tenant_id": tenant_id,
        "formato": resultado.get("formato", "desconocido"),
        "resultado": resultado,
    }

    st.session_state.material_history.insert(0, registro)


def mostrar_adaptacion():
    aplicar_estilos()

    st.markdown(
        """
    <div class="nm-hero">
        <h2>Adaptar contenido</h2>
        <p>
            Transforma documentos en materiales educativos
            interactivos y personalizados.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### Configuración del material")

    with st.form("formulario_adaptacion"):
        query = st.text_area(
            "Tema o pregunta",
            placeholder=(
                "Ejemplo: ¿Qué es Oracle AI Success Navigator " "y para qué sirve?"
            ),
            height=110,
        )

        tenant_id = st.text_input(
            "Espacio de trabajo", value=st.session_state.get("tenant_id", "equipo12")
        )

        col1, col2 = st.columns(2)

        with col1:
            perfil = st.selectbox(
                "Perfil de aprendizaje",
                ["principiante", "intermedio", "avanzado"],
                index=1,
            )

        with col2:
            formatos = {
                "Resumen": "resumen",
                "Flashcards": "flashcard",
                "Quiz": "quiz",
                "Guion": "guion",
                "Tutorial": "tutorial",
            }

            formato_visible = st.selectbox("Formato de salida", list(formatos.keys()))

        col_rag, col_items = st.columns(2)

        with col_rag:

            top_k = st.slider(
                "**Fragmentos de contexto (RAG)**",
                min_value=1,
                max_value=10,
                value=3,
                help="Define cuántos fragmentos de texto recuperados se utilizarán como contexto para generar la respuesta. Un valor mayor aporta más contexto, pero puede incluir información menos relevante.",
            )

        with col_items:

            cantidad_items = st.slider(
                "**Cantidad de elementos**",
                min_value=1,
                max_value=10,
                value=3,
                help="Define cuántos elementos (tarjetas, preguntas, escenas o pasos) generará la IA. En el formato Resumen se ignora este valor.",
            )

        enviar = st.form_submit_button(
            "Generar contenido", type="primary", use_container_width=True
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
                top_k=top_k,
                cantidad_items=cantidad_items,
            )

        if correcto:
            if not isinstance(resultado, dict):
                st.warning(
                    "No pudimos estructurar el material educativo en este intento. "
                    "Por favor, inténtalo de nuevo."
                )
                return

            st.session_state.resultado_adaptacion = resultado

            st.session_state.indice_flashcard = 0
            st.session_state.mostrar_respuesta_flashcard = False

            st.session_state.indice_quiz = 0

            guardar_en_libreria(
                resultado=resultado,
                query=query.strip(),
                perfil=perfil,
                tenant_id=tenant_id.strip(),
            )

            st.success("Material generado correctamente " "y agregado a la Librería.")

        else:
            st.error(str(resultado))
            return

    resultado_guardado = st.session_state.get("resultado_adaptacion")

    if resultado_guardado:
        mostrar_resultado(resultado_guardado)

        st.download_button(
            "Descargar material en JSON",
            data=json.dumps(resultado_guardado, ensure_ascii=False, indent=2),
            file_name="contenido_adaptado.json",
            mime="application/json",
            use_container_width=True,
        )
