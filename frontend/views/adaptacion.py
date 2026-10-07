import streamlit as st


def mostrar_adaptacion():
    st.title("✨ Adaptar contenido")

    st.write(
        "Selecciona cómo quieres transformar el contenido técnico."
    )

    formato = st.selectbox(
        "Formato de salida",
        [
            "Resumen",
            "Flashcards",
            "Quiz",
            "Guion"
        ]
    )

    st.selectbox(
        "Perfil de aprendizaje",
        [
            "General",
            "Principiante",
            "Intermedio",
            "Avanzado"
        ]
    )

    st.text_area(
        "Indicaciones adicionales",
        placeholder=(
            "Ejemplo: Explica los conceptos "
            "utilizando un lenguaje sencillo."
        ),
        height=120
    )

    st.info(
        "La interfaz está preparada. La generación se habilitará "
        "cuando el endpoint de adaptación esté disponible."
    )

    if st.button(
        "Generar contenido",
        type="primary",
        use_container_width=True
    ):
        st.warning(
            "El endpoint de adaptación todavía no está "
            "disponible en el backend actual."
        )

    st.caption(
        f"Formato seleccionado: {formato.lower()}"
    )