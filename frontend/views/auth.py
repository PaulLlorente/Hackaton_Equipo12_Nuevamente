
import streamlit as st

from services.api import iniciar_sesion, registrar_usuario


def cargar_estilos_auth():
    st.markdown(
        """
        <style>
        .auth-hero {
            max-width: 560px;
            margin: 8px auto 28px auto;
            text-align: center;
        }

        .auth-logo {
            width: 62px;
            height: 62px;
            margin: 0 auto 18px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 18px;
            background: linear-gradient(135deg, #a81780, #35dff2);
            color: #ffffff;
            font-size: 23px;
            font-weight: 800;
            letter-spacing: -1px;
            box-shadow:
                0 0 22px rgba(244, 78, 198, 0.22),
                0 0 35px rgba(53, 223, 242, 0.10);
        }

        .auth-hero h1 {
            margin: 0 0 10px 0;
            font-size: clamp(32px, 4vw, 43px) !important;
            font-weight: 800;
            letter-spacing: -1.3px;
            color: #f1f5ff !important;
            text-shadow: none !important;
        }

        .auth-hero h1 span {
            color: #f44ec6 !important;
        }

        .auth-hero p {
            margin: 0 auto;
            max-width: 490px;
            font-size: 14px;
            line-height: 1.8;
            color: #a7b7cd;
        }

        .auth-accent {
            width: 80px;
            height: 3px;
            margin: 18px auto 0 auto;
            border-radius: 10px;
            background: linear-gradient(90deg, #f44ec6, #35dff2);
        }

        .st-key-auth-panel {
            background: linear-gradient(
                145deg,
                rgba(23, 29, 50, 0.98),
                rgba(13, 20, 36, 0.98)
            );
            border: 1px solid #39415f;
            border-radius: 20px;
            padding: 28px;
            box-shadow:
                0 18px 48px rgba(0, 0, 0, 0.22),
                0 0 28px rgba(244, 78, 198, 0.05);
        }

        .st-key-auth-panel h3 {
            text-align: center;
            font-size: 21px !important;
            font-weight: 750;
            margin-bottom: 5px;
            color: #f1f5ff !important;
        }

        .st-key-auth-panel [data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 8px 0 0 0 !important;
        }

        .st-key-auth-panel [data-testid="stForm"]:hover {
            border-color: transparent !important;
        }

        .st-key-auth-panel [data-testid="stTextInput"] input {
            background: #0c1425 !important;
            color: #f1f5ff !important;
            border-radius: 10px !important;
            min-height: 44px;
        }

        .st-key-auth-panel [data-testid="stTextInput"] input:focus {
            border-color: #35dff2 !important;
            box-shadow:
                0 0 0 1px rgba(53, 223, 242, 0.20) !important;
        }

        .st-key-auth-panel .stFormSubmitButton button {
            min-height: 48px;
            border-radius: 11px !important;
            font-weight: 700;
            background: linear-gradient(
                110deg,
                #aa187f,
                #cb2ba7
            ) !important;
            border: 1px solid #f44ec6 !important;
            color: #ffffff !important;
        }

        .st-key-auth-panel .stFormSubmitButton button:hover {
            background: linear-gradient(
                110deg,
                #c51e95,
                #df3ab5
            ) !important;
            box-shadow:
                0 0 22px rgba(244, 78, 198, 0.30) !important;
        }

        .st-key-auth-panel .stButton button {
            min-height: 44px;
            border-radius: 11px !important;
            background: #111d30 !important;
            border: 1px solid #35dff2 !important;
            color: #d5faff !important;
        }

        .st-key-auth-panel .stButton button:hover {
            background: #172a3b !important;
            border-color: #35dff2 !important;
            box-shadow:
                0 0 16px rgba(53, 223, 242, 0.18) !important;
        }

        .auth-footer {
            margin-top: 18px;
            margin-bottom: 10px;
            text-align: center;
            font-size: 13px;
            color: #a7b7cd;
        }

        .auth-caption {
            margin-top: 14px;
            text-align: center;
            font-size: 12px;
            color: #71849f;
        }

        @media (max-width: 768px) {
            .auth-hero {
                margin-top: 0;
                margin-bottom: 22px;
            }

            .auth-logo {
                width: 54px;
                height: 54px;
                font-size: 20px;
            }

            .st-key-auth-panel {
                padding: 18px;
                border-radius: 16px;
            }

            .auth-hero p {
                font-size: 13px;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            .st-key-auth-panel button {
                transition: none !important;
                transform: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def mostrar_encabezado(descripcion):
    st.markdown(
        f"""
        <div class="auth-hero">
            <div class="auth-logo">NM</div>
            <h1>Nueva<span>Mente</span></h1>
            <p>{descripcion}</p>
            <div class="auth-accent"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_login():
    cargar_estilos_auth()

    mostrar_encabezado(
        "Convierte documentación técnica en contenido claro, "
        "útil y adaptado a diferentes formas de aprendizaje."
    )

    _, centro, _ = st.columns([1, 1.5, 1])

    with centro:
        with st.container(key="auth-panel"):
            st.subheader("Iniciar sesión")

            if st.session_state.get("mensaje_registro_exitoso"):
                st.success(st.session_state.mensaje_registro_exitoso)
                st.session_state.mensaje_registro_exitoso = None

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
                        if (
                            isinstance(resultado, dict)
                            and resultado.get("access_token")
                        ):
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

            st.markdown(
                """
                <div class="auth-footer">
                    ¿Aún no tienes una cuenta?
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Crear cuenta",
                use_container_width=True,
                key="ir_registro"
            ):
                st.session_state.pantalla_auth = "registro"
                st.rerun()

        st.markdown(
            """
            <div class="auth-caption">
                NuevaMente · Plataforma de aprendizaje inteligente
            </div>
            """,
            unsafe_allow_html=True
        )


def mostrar_registro():
    cargar_estilos_auth()

    mostrar_encabezado(
        "Crea tu cuenta y comienza a transformar "
        "documentación técnica en experiencias de aprendizaje."
    )

    _, centro, _ = st.columns([1, 1.5, 1])

    with centro:
        with st.container(key="auth-panel"):
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
                        st.session_state.mensaje_registro_exitoso = (
                            "Tu cuenta fue creada correctamente. "
                            "Ahora puedes iniciar sesión."
                        )
                        st.session_state.pantalla_auth = "login"
                        st.rerun()

                    else:
                        st.error(str(resultado))

            if st.button(
                "Volver a iniciar sesión",
                use_container_width=True,
                key="volver_login"
            ):
                st.session_state.pantalla_auth = "login"
                st.rerun()

        st.markdown(
            """
            <div class="auth-caption">
                NuevaMente · Plataforma de aprendizaje inteligente
            </div>
            """,
            unsafe_allow_html=True
        )
