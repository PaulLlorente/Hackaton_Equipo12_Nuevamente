
import re
import streamlit as st

from services.api import consultar_rag


def limpiar_texto(texto):
    texto = str(texto or "").strip()

    texto = re.sub(
        r'^\s*"?texto"?\s*:\s*"',
        "",
        texto
    )

    texto = texto.rstrip()

    if texto.endswith('"'):
        texto = texto[:-1]

    return texto.strip()


def mostrar_consulta():
    st.title("Consultar documento")
    st.write("Haz una pregunta sobre la información que ha sido procesada.")

    tenant_id = st.text_input(
        "Espacio de consulta",
        value=st.session_state.get("tenant_id", "equipo12")
    )

    pregunta = st.text_area(
        "¿Qué quieres saber?",
        placeholder="Escribe tu pregunta sobre el documento...",
        height=100
    )

    if st.button("Consultar", use_container_width=True):
        if not pregunta.strip():
            st.warning("Escribe una pregunta para continuar.")
            return

        if not tenant_id.strip():
            st.warning("Ingresa un espacio de consulta.")
            return

        with st.spinner("Buscando información en los documentos..."):
            exito, respuesta = consultar_rag(
                pregunta.strip(),
                tenant_id.strip()
            )

        if not exito:
            st.error(str(respuesta))
            return

        if not isinstance(respuesta, dict):
            st.error("El servidor devolvió una respuesta inesperada.")
            return

        resultados = respuesta.get("results", [])

        if not resultados:
            st.info(
                "No se encontraron fragmentos relacionados "
                "con tu pregunta."
            )
            return

        st.success(
            f"Consulta realizada correctamente. "
            f"Se encontraron {len(resultados)} fragmentos."
        )

        st.subheader("Información encontrada")

        for indice, resultado in enumerate(resultados, start=1):
            texto = limpiar_texto(resultado.get("text", ""))
            metadata = resultado.get("metadata") or {}

            origen = metadata.get(
                "origen",
                "Documento sin nombre"
            )

            document_id = metadata.get(
                "document_id",
                "No disponible"
            )

            with st.container(border=True):
                st.markdown(f"**Fragmento {indice}**")

                st.write(
                    texto if texto else "Sin contenido disponible."
                )

                st.caption(f"Documento: {origen}")

                with st.expander("Ver detalles"):
                    st.write(f"Document ID: {document_id}")
                    st.write(
                        f"Tenant: {metadata.get('tenant_id', tenant_id)}"
                    )

        with st.expander("Ver respuesta completa del servidor"):
            st.json(respuesta)
