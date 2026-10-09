import streamlit as st


def cargar_estilos():
    st.markdown(
        """
        <style>

        :root {
            --background: #f7f8fa;
            --surface: #ffffff;
            --primary: #30343b;
            --text: #252932;
            --muted: #858b96;
            --border: #e1e4e8;
        }

        .stApp {
            background: var(--background);
            color: var(--text);
        }

        .block-container {
            max-width: 1250px;
            padding-top: 3rem;
            padding-bottom: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        html, body {
            font-family: "Segoe UI", Arial, sans-serif;
        }

        h1, h2, h3 {
            color: var(--text);
            letter-spacing: -0.5px;
        }

        h1 {
            font-size: 35px !important;
            font-weight: 700 !important;
        }

        h2 {
            font-size: 25px !important;
            font-weight: 700 !important;
        }

        h3 {
            font-size: 19px !important;
            font-weight: 650 !important;
        }

        p {
            color: #656c78;
        }

        /* SIDEBAR */

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 13px;
            padding: 18px 5px 12px;
        }

        .brand-logo {
            width: 43px;
            height: 43px;
            background: #30343b;
            color: #ffffff;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 1px;
        }

        .brand-name {
            font-size: 19px;
            font-weight: 750;
            color: #242831;
        }

        .brand-subtitle {
            font-size: 11px;
            color: #9ba1aa;
            margin-top: 3px;
        }

        .sidebar-label {
            color: #a0a5ae;
            font-size: 11px;
            letter-spacing: 1.3px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        [data-testid="stSidebar"] hr {
            border-color: #e9eaed;
            margin: 24px 0;
        }

        /* NAVEGACION */

        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 7px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            padding: 12px 14px;
            border-radius: 8px;
            transition: background 0.2s;
            cursor: pointer;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: #f3f4f6;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(
            input:checked
        ) {
            background: #edeef0;
            font-weight: 650;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            display: none;
        }

        /* ENCABEZADO */

        .page-header {
            margin-bottom: 30px;
        }

        .page-header h1 {
            margin-top: 5px;
            margin-bottom: 8px;
        }

        .page-header p {
            color: #9399a3;
            font-size: 15px;
            margin: 0;
        }

        .eyebrow {
            color: #9097a1;
            font-size: 11px;
            letter-spacing: 1.4px;
            font-weight: 750;
        }

        /* TARJETAS */

        .card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }

        .card h3 {
            margin-top: 0;
        }

        .card p {
            line-height: 1.7;
            color: #777e89;
        }

        /* METRICAS */

        .metric-card {
            background: #ffffff;
            border: 1px solid #d9dde2;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 22px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }

        .metric-title {
            background: #f0f1f2;
            padding: 18px 22px;
            border-bottom: 1px solid #d9dde2;
            font-size: 14px;
            font-weight: 750;
            color: #30343b;
        }

        .metric-number {
            text-align: center;
            font-size: 65px;
            font-weight: 750;
            color: #262a32;
            padding-top: 25px;
            letter-spacing: -2px;
        }

        .metric-description {
            text-align: center;
            color: #a0a6af;
            font-size: 13px;
            padding: 5px 15px 28px;
        }

        /* BOTONES */

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 7px;
            min-height: 45px;
            font-weight: 650;
            transition: 0.2s ease;
        }

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: #383d46;
            border: 1px solid #383d46;
            color: white;
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background: #272b32;
            border-color: #272b32;
        }

        .stButton > button[kind="secondary"] {
            background: white;
            border: 1px solid #d5d9df;
            color: #30343b;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #f1f2f4;
            border-color: #aeb4bd;
        }

        /* ACTIVIDAD RECIENTE */

        .recent-item {
            background: #ffffff;
            border: 1px solid #dfe2e6;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 9px;
            min-height: 75px;
        }

        .recent-title {
            font-size: 15px;
            font-weight: 700;
            color: #292d35;
        }

        .recent-subtitle {
            font-size: 13px;
            color: #a0a5ae;
            margin-top: 4px;
        }

        /* FORMULARIOS */

        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid #dfe2e6;
            border-radius: 10px;
            padding: 25px;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background: #ffffff;
            color: #252932;
            border: 1px solid #cfd4db;
            border-radius: 7px;
        }

        [data-baseweb="select"] > div {
            background: #ffffff;
            border-color: #cfd4db;
            border-radius: 7px;
        }

        /* ARCHIVOS */

        [data-testid="stFileUploader"] {
            background: #ffffff;
            border: 2px dashed #c4c9d0;
            border-radius: 12px;
            padding: 20px;
        }

        /* PESTAÑAS */

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            background: white;
            border: 1px solid #d9dde2;
            border-radius: 7px;
            padding: 10px 22px;
        }

        .stTabs [aria-selected="true"] {
            background: #383d46;
            color: white;
        }

        /* OTROS */

        [data-testid="stAlert"] {
            border-radius: 8px;
        }

        hr {
            border: none;
            border-top: 1px solid #e3e6e9;
        }

        .dashboard-footer {
            text-align: center;
            color: #b0b5bd;
            font-size: 12px;
            padding: 25px 0;
        }

        @media (max-width: 768px) {
            .block-container {
                padding: 1.5rem 1rem;
            }

            .metric-number {
                font-size: 48px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )