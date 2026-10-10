
import streamlit as st

from services.api import iniciar_sesion, registrar_usuario


def mostrar_login():
    st.markdown(
        """
        <div class="hero">
            <h1>NuevaMente</h1>
            <p>
                Convierte documentación técnica en contenido claro,
                útil y adaptado a diferentes formas de aprendizaje.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, centro, _ = st.columns([1, 1.4, 1])

    with centro:
        st.subheader("Iniciar sesión")

        with st.form("form_login"):
            email = st.text_input(
                "Correo electrónico",
                placeholder="correo@ejemplo.com"
            )

            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Tu contraseña"
            )

            enviar = st.form_submit_button(
                "Iniciar sesión",
                use_container_width=True
            )

        if enviar:
            if not email.strip() or not password:
                st.warning("Ingresa tu correo y contraseña.")
            else:
                with st.spinner("Iniciando sesión..."):
                    correcto, resultado = iniciar_sesion(
                        email.strip(),
                        password
                    )

                if correcto:
                    if isinstance(resultado, dict) and resultado.get("access_token"):
                        st.session_state.token = resultado["access_token"]
                        st.session_state.email = email.strip()
                        st.session_state.rol = resultado.get(
                            "rol",
                            resultado.get("role", "usuario")
                        )
                        st.session_state.pagina = "Dashboard"
                        st.rerun()
                    else:
                        st.error(
                            "El servidor no devolvió un token de acceso válido."
                        )
                else:
                    st.error(str(resultado))

        st.write("¿Aún no tienes una cuenta?")

        if st.button(
            "Crear cuenta",
            use_container_width=True,
            key="ir_registro"
        ):
            st.session_state.pantalla_auth = "registro"
            st.rerun()


def mostrar_registro():
    st.markdown(
        """
        <div class="hero">
            <h1>NuevaMente</h1>
            <p>
                Crea tu cuenta para comenzar a trabajar
                con documentación técnica.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, centro, _ = st.columns([1, 1.4, 1])

    with centro:
        st.subheader("Crear cuenta")

        with st.form("form_registro"):
            email = st.text_input(
                "Correo electrónico",
                placeholder="correo@ejemplo.com"
            )

            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Crea una contraseña"
            )

            confirmar = st.text_input(
                "Confirmar contraseña",
                type="password",
                placeholder="Repite tu contraseña"
            )

            enviar = st.form_submit_button(
                "Registrarme",
                use_container_width=True
            )

        if enviar:
            if not email.strip() or not password or not confirmar:
                st.warning("Completa todos los campos.")

            elif password != confirmar:
                st.error("Las contraseñas no coinciden.")

            else:
                with st.spinner("Creando cuenta..."):
                    correcto, resultado = registrar_usuario(
                        email.strip(),
                        password
                    )

                if correcto:
                    st.success("Tu cuenta fue creada correctamente.")
                    st.session_state.pantalla_auth = "login"
                    st.info("Ahora puedes iniciar sesión.")
                else:
                    st.error(str(resultado))

        if st.button(
            "Volver a iniciar sesión",
            use_container_width=True,
            key="volver_login"
        ):
            st.session_state.pantalla_auth = "login"
            st.rerun()
