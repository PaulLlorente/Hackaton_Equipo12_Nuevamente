import streamlit as st
from html import escape


def mostrar_cuenta():
    st.title("Mi cuenta")

    email = escape(str(st.session_state.get("email") or "Sin información"))
    rol = escape(str(st.session_state.get("rol") or "usuario"))
    tenant_id = escape(str(st.session_state.get("tenant_id") or "Sin asignar"))

    st.markdown(
        f"""
        <div class="card">
            <h3>Información de la sesión</h3>
            <p><b>Correo:</b> {email}</p>
            <p><b>Rol:</b> {rol}</p>
            <p><b>Espacio de trabajo:</b> {tenant_id}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Información correspondiente a la sesión actual."
    )