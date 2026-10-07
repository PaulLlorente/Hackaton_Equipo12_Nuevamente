import streamlit as st


def mostrar_cuenta():
    st.title("👤 Mi cuenta")

    st.markdown(
        f"""
        <div class="card">
            <h3>Información de la sesión</h3>
            <p><b>Correo:</b> {st.session_state.email}</p>
            <p><b>Rol:</b> {st.session_state.rol}</p>
            <p><b>Tenant actual:</b> {st.session_state.tenant_id}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "El token de autenticación se mantiene únicamente "
        "durante la sesión de Streamlit."
    )