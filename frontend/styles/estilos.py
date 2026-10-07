import streamlit as st


def cargar_estilos():
    st.markdown(
        """
        <style>

        .stApp {
            background:
                radial-gradient(
                    circle at 20% 20%,
                    rgba(91, 82, 255, 0.12),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 80% 10%,
                    rgba(0, 190, 255, 0.08),
                    transparent 25%
                ),
                #0b1020;

            color: #f8fafc;
        }

        [data-testid="stSidebar"] {
            background: #11182b;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        .hero {
            padding: 38px;
            border-radius: 24px;

            background:
                linear-gradient(
                    135deg,
                    rgba(91,82,255,0.28),
                    rgba(0,190,255,0.10)
                );

            border: 1px solid rgba(255,255,255,0.10);
            margin-bottom: 25px;
        }

        .hero h1 {
            font-size: 46px;
            margin-bottom: 8px;
            color: white;
        }

        .hero p {
            font-size: 18px;
            color: #cbd5e1;
            margin-bottom: 0;
        }

        .card {
            padding: 25px;
            border-radius: 20px;
            background: rgba(17,24,43,0.85);
            border: 1px solid rgba(255,255,255,0.08);
            min-height: 180px;
            margin-bottom: 15px;
        }

        .card h3 {
            margin-top: 0;
            color: white;
        }

        .card p {
            color: #aeb8cc;
        }

        .status {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            background: rgba(34,197,94,0.12);
            color: #86efac;
            font-size: 13px;
            margin-bottom: 15px;
        }

        .small-text {
            color: #94a3b8;
            font-size: 14px;
        }

        div[data-testid="stForm"] {
            background: rgba(17,24,43,0.82);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="stFileUploader"] {
            border-radius: 16px;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 12px;
            min-height: 45px;
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )