
import streamlit as st

from styles.estilos import cargar_estilos
from views.auth import mostrar_login, mostrar_registro
from views.inicio import mostrar_inicio
from views.carga import mostrar_carga
from views.consulta import mostrar_consulta
from views.adaptacion import mostrar_adaptacion
from views.cuenta import mostrar_cuenta


MODO_DEMO = False


st.set_page_config(
    page_title="NuevaMente | Panel Administrativo",
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
        "documentos": [],
        "material_history": [],
        "pagina": "Dashboard"
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
    st.session_state.material_history = []
    st.session_state.pantalla_auth = "login"
    st.session_state.pagina = "Dashboard"

    st.rerun()


def mostrar_aplicacion():
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-logo">NM</div>
                <div>
                    <div class="brand-name">NuevaMente</div>
                    <div class="brand-subtitle">
                        Plataforma de aprendizaje
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-label">NAVEGACIÓN</div>',
            unsafe_allow_html=True
        )

        opciones = [
            "Dashboard",
            "Cargar documento",
            "Consultar documento",
            "Adaptar contenido",
            "Librería",
            "Mi cuenta"
        ]

        if st.session_state.pagina not in opciones:
            st.session_state.pagina = "Dashboard"

        opcion = st.radio(
            "Navegación",
            opciones,
            key="pagina",
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-label">ESPACIO DE TRABAJO</div>',
            unsafe_allow_html=True
        )

        st.caption(
            f"Tenant: {st.session_state.tenant_id}"
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-label">CUENTA</div>',
            unsafe_allow_html=True
        )

        st.write(
            st.session_state.email or "Sin sesión"
        )

        st.caption(
            f"Rol: {st.session_state.rol or 'Sin asignar'}"
        )

        if MODO_DEMO:
            st.caption("Modo demostración")
        else:
            if st.button(
                "Cerrar sesión",
                use_container_width=True
            ):
                cerrar_sesion()

    if opcion == "Dashboard":
        mostrar_inicio()

    elif opcion == "Cargar documento":
        mostrar_carga()

    elif opcion == "Consultar documento":
        mostrar_consulta()

    elif opcion == "Adaptar contenido":
        mostrar_adaptacion()

    elif opcion == "Librería":
        mostrar_libreria()

    elif opcion == "Mi cuenta":
        mostrar_cuenta()


def mostrar_libreria():
    st.title("Librería de contenidos")

    st.write(
        "Consulta los materiales educativos generados "
        "durante esta sesión."
    )

    historial = st.session_state.material_history

    if not historial:
        st.info(
            "Todavía no hay materiales generados "
            "en esta sesión."
        )
        return

    for indice, material in enumerate(historial):
        titulo = material.get(
            "archivo",
            f"Material {indice + 1}"
        )

        formato = material.get(
            "formato",
            "Sin formato"
        )

        fecha = material.get(
            "fecha",
            "Sin fecha"
        )

        with st.expander(
            f"{titulo} - {formato} ({fecha})"
        ):
            st.write(
                f"**Perfil:** {material.get('perfil', 'No especificado')}"
            )

            st.write(
                f"**Formato:** {formato}"
            )

            resultado = material.get("resultado")

            if resultado is not None:
                st.json(resultado)

                import json

                st.download_button(
                    "Descargar JSON",
                    data=json.dumps(
                        resultado,
                        ensure_ascii=False,
                        indent=2
                    ),
                    file_name=f"material_{indice + 1}.json",
                    mime="application/json",
                    key=f"descargar_material_{indice}"
                )
            else:
                st.caption(
                    "Este registro no contiene "
                    "un resultado descargable."
                )


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
