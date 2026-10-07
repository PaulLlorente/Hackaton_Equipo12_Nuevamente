import streamlit as st

from services.api import consultar_rag


def mostrar_consulta():
    st.title("🔎 Consultar documento")

    st.write(
        "Haz una pregunta sobre la información que ha sido procesada."
    )

    tenant_id = st.text_input(
        "Espacio de consulta",
        value=st.session_state.tenant_id,
        key="tenant_busqueda"
    )

    pregunta = st.text_area(
        "¿Qué quieres saber?",
        placeholder=(
            "Ejemplo: ¿Cuáles son los conceptos "
            "principales del documento?"
        ),
        height=130
    )

    if st.button(
        "Consultar",
        type="primary",
        use_container_width=True
    ):
        tenant_id = tenant_id.strip()
        pregunta = pregunta.strip()

        if not tenant_id:
            st.warning(
                "Ingresa el identificador del espacio."
            )

        elif not pregunta:
            st.warning("Escribe una pregunta.")

        else:
            st.session_state.tenant_id = tenant_id

            with st.spinner("Buscando información..."):
                correcto, resultado = consultar_rag(
                    pregunta,
                    tenant_id
                )

            if correcto:
                st.success("Consulta realizada.")
                st.subheader("Resultado")

                if isinstance(resultado, dict):
                    if "respuesta" in resultado:
                        st.write(resultado["respuesta"])

                    elif "answer" in resultado:
                        st.write(resultado["answer"])

                    elif "results" in resultado:
                        st.write(resultado["results"])

                    else:
                        st.json(resultado)

                else:
                    st.write(resultado)

                with st.expander("Ver respuesta completa"):
                    st.json(resultado)

            else:
                st.error(resultado)