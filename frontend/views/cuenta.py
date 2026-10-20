
import streamlit as st
from html import escape
from textwrap import dedent


def mostrar_cuenta():

    # Obtener los datos reales de la sesión
    email = escape(
        str(st.session_state.get("email") or "Sin información")
    )

    rol = escape(
        str(st.session_state.get("rol") or "usuario")
    )

    tenant_id = escape(
        str(st.session_state.get("tenant_id") or "Sin asignar")
    )

    # Estilos exclusivos de la pantalla Mi cuenta
    st.markdown(
        """
<style>
.cuenta-hero {
    background: linear-gradient(
        115deg,
        #281431,
        #151b35 58%,
        #0b2132
    );
    border: 1px solid #503258;
    border-radius: 20px;
    padding: 34px 40px;
    margin-bottom: 26px;
}

.cuenta-etiqueta {
    color: #35dff2;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.cuenta-hero h1 {
    color: #f1f5ff !important;
    font-size: 38px !important;
    font-weight: 800 !important;
    margin: 0 0 12px !important;
}

.cuenta-hero h1 span {
    color: #f44ec6;
}

.cuenta-hero p {
    color: #b8c8e3;
    font-size: 15px;
    margin: 0;
}

.cuenta-panel {
    background: #141c30;
    border: 1px solid #34415c;
    border-radius: 18px;
    padding: 30px;
}

.cuenta-perfil {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 25px;
}

.cuenta-avatar {
    width: 70px;
    height: 70px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #b8249a,
        #2789b9
    );
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 27px;
    font-weight: 800;
    flex-shrink: 0;
}

.cuenta-perfil-info {
    flex: 1;
    min-width: 0;
}

.cuenta-perfil-info h2 {
    color: #f1f5ff !important;
    margin: 0 0 5px !important;
    font-size: 23px !important;
}

.cuenta-perfil-info p {
    color: #91a4bf;
    margin: 0;
    font-size: 13px;
}

.cuenta-estado {
    color: #8af0c4;
    background: #123a35;
    border: 1px solid #246c5d;
    border-radius: 20px;
    padding: 7px 13px;
    font-size: 12px;
    white-space: nowrap;
}

.cuenta-linea {
    border: none;
    border-top: 1px solid #34415c;
    margin: 20px 0;
}

.cuenta-grid {
    display: grid;
    grid-template-columns: repeat(
        2,
        minmax(0, 1fr)
    );
    gap: 16px;
}

.cuenta-dato {
    background: #0c1425;
    border: 1px solid #34415c;
    border-radius: 12px;
    padding: 19px;
    min-width: 0;
}

.cuenta-dato-label {
    color: #35dff2;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 12px;
}

.cuenta-dato-valor {
    color: #f1f5ff;
    font-size: 15px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.cuenta-nota {
    color: #91a4bf;
    font-size: 12px;
    margin-top: 22px;
}

@media (max-width: 700px) {
    .cuenta-hero {
        padding: 24px;
    }

    .cuenta-panel {
        padding: 20px;
    }

    .cuenta-grid {
        grid-template-columns: 1fr;
    }

    .cuenta-perfil {
        flex-wrap: wrap;
    }
}
</style>
        """.strip(),
        unsafe_allow_html=True,
    )

    # Encabezado de Mi cuenta
    html_encabezado = """
<div class="cuenta-hero">
    <div class="cuenta-etiqueta">PERFIL DE USUARIO</div>
    <h1>Mi <span>cuenta</span></h1>
    <p>
        Consulta la información de tu perfil
        y los datos de tu sesión actual.
    </p>
</div>
"""

    st.markdown(
        dedent(html_encabezado).strip(),
        unsafe_allow_html=True,
    )

    # Tarjeta con información de la sesión
    html_perfil = f"""
<div class="cuenta-panel">
    <div class="cuenta-perfil">
        <div class="cuenta-avatar">NM</div>
        <div class="cuenta-perfil-info">
            <h2>Mi perfil</h2>
            <p>Información de la sesión</p>
        </div>
        <span class="cuenta-estado">Sesión activa</span>
    </div>
    <hr class="cuenta-linea">
    <div class="cuenta-grid">
        <div class="cuenta-dato">
            <div class="cuenta-dato-label">CORREO ELECTRÓNICO</div>
            <div class="cuenta-dato-valor">{email}</div>
        </div>
        <div class="cuenta-dato">
            <div class="cuenta-dato-label">ROL DE USUARIO</div>
            <div class="cuenta-dato-valor">{rol}</div>
        </div>
        <div class="cuenta-dato">
            <div class="cuenta-dato-label">ESPACIO DE TRABAJO</div>
            <div class="cuenta-dato-valor">{tenant_id}</div>
        </div>
    </div>
    <div class="cuenta-nota">
        Los datos mostrados corresponden a tu sesión actual.
    </div>
</div>
"""

    st.markdown(
        dedent(html_perfil).strip(),
        unsafe_allow_html=True,
    )
