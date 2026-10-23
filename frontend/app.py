import json
import streamlit as st

from styles.estilos import cargar_estilos
from views.auth import mostrar_login, mostrar_registro
from views.inicio import mostrar_inicio
from views.carga import mostrar_carga
from views.consulta import mostrar_consulta
from views.adaptacion import aplicar_estilos, mostrar_adaptacion, mostrar_resultado
from views.cuenta import mostrar_cuenta

st.set_page_config(
    page_title="NuevaMente | Panel Administrativo",
    layout="wide",
    initial_sidebar_state="expanded",
)

cargar_estilos()
aplicar_estilos()


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
        "consulta_historial": [],
        "pagina": "Dashboard",
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
    st.session_state.consulta_historial = []
    st.session_state.material_libreria_activo = None
    st.session_state.resultado_consulta = None
    st.session_state.resultado_adaptacion = None
    st.session_state.pantalla_auth = "login"
    st.session_state.ir_a = "Dashboard"

    for clave_sensible in (
        "login_email",
        "login_password",
        "registro_email",
        "registro_password",
        "registro_confirmar",
    ):
        st.session_state.pop(clave_sensible, None)

    st.rerun()


def mostrar_aplicacion():
    if st.session_state.get("ir_a"):
        st.session_state.pagina = st.session_state.ir_a
        st.session_state.ir_a = None

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
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-label">NAVEGACIÓN</div>', unsafe_allow_html=True
        )

        opciones = [
            "Dashboard",
            "Cargar documento",
            "Adaptar contenido",
            "Librería",
            "Consultar documento",
            "Mi cuenta",
        ]

        if st.session_state.pagina not in opciones:
            st.session_state.pagina = "Dashboard"

        opcion = st.radio(
            "Navegación", opciones, key="pagina", label_visibility="collapsed"
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-label">ESPACIO DE TRABAJO</div>',
            unsafe_allow_html=True,
        )

        st.caption(f"Tenant: {st.session_state.tenant_id}")

        st.divider()

        st.markdown('<div class="sidebar-label">CUENTA</div>', unsafe_allow_html=True)

        st.write(st.session_state.email or "Sin sesión")

        st.caption(f"Rol: {st.session_state.rol or 'Sin asignar'}")

        st.button("Cerrar sesión", on_click=cerrar_sesion, use_container_width=True)

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

def cerrar_visor_libreria():
    st.session_state.material_libreria_activo = None


@st.dialog(
    "📖 Visualizador de contenido interactivo",
    width="large",
    on_dismiss=cerrar_visor_libreria,
)
def abrir_visor_modal(resultado):
    mostrar_resultado(resultado)
    st.divider()
    if st.button("✕ Cerrar ventana", key="cerrar_visor_lib", use_container_width=True):
        st.session_state.material_libreria_activo = None
        st.rerun()


def mostrar_libreria():
    st.title("Librería de contenidos")

    st.write("Consulta los materiales educativos generados durante esta sesión.")

    historial = list(st.session_state.material_history)

    if not historial:
        st.info("Todavía no hay materiales generados en esta sesión.")
        return

    opciones_filtro = {
        "Todos": None,
        "Resumen": "resumen",
        "Flashcards": "flashcard",
        "Quiz": "quiz",
        "Guion": "guion",
        "Tutorial": "tutorial",
    }

    iconos_formato = {
        "resumen": "📄 Resumen",
        "flashcard": "🗂️ Flashcards",
        "quiz": "❓ Quiz",
        "guion": "🎬 Guion",
        "tutorial": "🛠️ Tutorial",
    }

    col_busqueda, col_filtro = st.columns([1, 1])

    with col_busqueda:
        busqueda = st.text_input(
            "Buscar material",
            placeholder="🔍 Buscar por tema, concepto clave o perfil...",
        )

    with col_filtro:
        filtro_seleccionado = st.pills(
            "Filtrar por formato",
            list(opciones_filtro.keys()),
            default="Todos",
        )

    formato_clave = opciones_filtro.get(filtro_seleccionado)
    termino = busqueda.strip().lower()

    materiales_visibles = []
    for material in historial:
        cumple_formato = (
            formato_clave is None or material.get("formato") == formato_clave
        )

        resultado_mat = material.get("resultado") or {}
        texto_buscable = " ".join(
            [
                str(material.get("archivo") or ""),
                str(material.get("perfil") or ""),
                str(resultado_mat.get("titulo") or ""),
                str(resultado_mat.get("conceptos_clave") or ""),
            ]
        ).lower()

        cumple_busqueda = not termino or termino in texto_buscable

        if cumple_formato and cumple_busqueda:
            materiales_visibles.append(material)

    if not materiales_visibles:
        st.info(
            "No se encontraron materiales que coincidan con los filtros seleccionados."
        )
        return

    # Renderizado en casillas / tarjetas (cuadrícula de 3 columnas)
    for i in range(0, len(materiales_visibles), 3):
        fila = st.columns(3)
        for col_idx, col in enumerate(fila):
            idx_item = i + col_idx
            if idx_item < len(materiales_visibles):
                material = materiales_visibles[idx_item]
                formato_raw = material.get("formato", "desconocido")
                badge_formato = iconos_formato.get(
                    formato_raw, f"📄 {formato_raw.capitalize()}"
                )
                fecha = material.get("fecha", "Sin fecha")
                tema = material.get("archivo", f"Material {idx_item + 1}")
                resultado = material.get("resultado") or {}
                titulo_ai = resultado.get("titulo")

                with col:
                    with st.container(border=True):
                        col_tag, col_fec = st.columns([1, 1])
                        with col_tag:
                            st.caption(f"**{badge_formato}**")
                        with col_fec:
                            st.caption(
                                f"<div style='text-align: right; color: #8892b0;'>⏱️ {fecha}</div>",
                                unsafe_allow_html=True,
                            )

                        # Título del tema consultado
                        st.markdown(f"### {tema}")

                        # Subtítulo pedagógico si la IA generó uno
                        if titulo_ai and titulo_ai != tema:
                            st.caption(f"💡 *{titulo_ai}*")

                        st.caption(
                            f"👤 **Perfil:** {material.get('perfil', 'General')} | 🏢 **Espacio:** `{material.get('tenant_id', 'default')}`"
                        )

                        st.divider()

                        c_btn1, c_btn2 = st.columns(2)
                        with c_btn1:
                            if st.button(
                                "👁️ Visualizar",
                                key=f"ver_lib_{idx_item}_{formato_raw}",
                                type="primary",
                                use_container_width=True,
                            ):
                                st.session_state.material_libreria_activo = resultado
                                st.session_state.indice_flashcard = 0
                                st.session_state.mostrar_respuesta_flashcard = False
                                st.session_state.indice_quiz = 0

                        with c_btn2:
                            st.download_button(
                                "📥 JSON",
                                data=json.dumps(
                                    resultado, ensure_ascii=False, indent=2
                                ),
                                file_name=f"material_{idx_item + 1}.json",
                                mime="application/json",
                                key=f"descargar_lib_{idx_item}_{formato_raw}",
                                use_container_width=True,
                            )

    # Ventana modal sobrepuesta cuando hay un material activo
    if st.session_state.get("material_libreria_activo"):
        abrir_visor_modal(st.session_state.material_libreria_activo)


def main():
    inicializar_sesion()

    contenedor_principal = st.empty()

    with contenedor_principal.container():
        if st.session_state.token:
            mostrar_aplicacion()

        elif st.session_state.pantalla_auth == "registro":
            mostrar_registro()

        else:
            mostrar_login()


if __name__ == "__main__":
    main()
