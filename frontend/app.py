import streamlit as st

from styles.estilos import cargar_estilos
from views.auth import mostrar_login, mostrar_registro
from views.inicio import mostrar_inicio
from views.carga import mostrar_carga
from views.consulta import mostrar_consulta
from views.adaptacion import mostrar_adaptacion
from views.cuenta import mostrar_cuenta


st.set_page_config(
    page_title="NuevaMente",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

cargar_estilos()


def inicializar_sesion():
    valores_iniciales = {
        "token": None,
        "rol": None,
        "email": None,
        "pantalla_auth": "login",
        "tenant_id": "equipo12",
        "document_id": None,
        "documentos": []
    }

    for clave, valor in valores_iniciales.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def cerrar_sesion():
    st.session_state.token = None
    st.session_state.rol = None
    st.session_state.email = None
    st.session_state.document_id = None
    st.session_state.documentos = []
    st.session_state.pantalla_auth = "login"

    st.rerun()


def mostrar_aplicacion():
    with st.sidebar:
        st.title("🧠 NuevaMente")

        st.caption(
            "Plataforma de aprendizaje adaptativo"
        )

        st.divider()

        opcion = st.radio(
            "Navegación",
            [
                "Inicio",
                "Cargar documento",
                "Consultar documento",
                "Adaptar contenido",
                "Mi cuenta"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.caption("Sesión")

        st.write(
            f"👤 {st.session_state.email}"
        )

        st.write(
            f"Rol: **{st.session_state.rol}**"
        )

        if st.button(
            "Cerrar sesión",
            use_container_width=True
        ):
            cerrar_sesion()

    if opcion == "Inicio":
        mostrar_inicio()

    elif opcion == "Cargar documento":
        mostrar_carga()

    elif opcion == "Consultar documento":
        mostrar_consulta()

    elif opcion == "Adaptar contenido":
        mostrar_adaptacion()

    elif opcion == "Mi cuenta":
        mostrar_cuenta()


def main():
    inicializar_sesion()

    if st.session_state.token:
        mostrar_aplicacion()

    elif st.session_state.pantalla_auth == "registro":
        mostrar_registro()

    else:
        mostrar_login()


if __name__ == "__main__":
    main()