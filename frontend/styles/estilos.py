
import streamlit as st


def cargar_estilos():
    st.markdown(
        """
        <style>
        :root {
            --background: #080d19;
            --surface: #141c30;
            --surface-hover: #1b2740;
            --primary: #f44ec6;
            --secondary: #35dff2;
            --text: #f1f5ff;
            --muted: #a7b7cd;
            --border: #303b56;
        }

        html, body {
            font-family: "Segoe UI", Arial, sans-serif;
            color-scheme: dark;
        }

        .stApp {
            background:
                radial-gradient(ellipse at 85% 10%, rgba(180,35,155,.10), transparent 40%),
                radial-gradient(ellipse at 5% 85%, rgba(22,185,215,.08), transparent 45%),
                var(--background);
            color: var(--text);
        }

        .block-container {
            max-width: 1250px;
            padding: 3rem;
        }

        h1, h2, h3 {
            color: var(--text) !important;
            letter-spacing: -.5px;
        }

        h1 {
            font-size: 35px !important;
            font-weight: 700 !important;
            text-shadow: 0 0 22px rgba(244,78,198,.18);
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
            color: var(--muted);
        }

        /* SIDEBAR */

        [data-testid="stSidebar"] {
            background: #0c1221;
            border-right: 1px solid #39304e;
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
            background: linear-gradient(135deg, #c51d94, #17b8d1);
            color: #fff;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 1px;
            box-shadow:
                0 0 12px rgba(244,78,198,.25),
                0 0 24px rgba(53,223,242,.12);
        }

        .brand-name {
            font-size: 19px;
            font-weight: 750;
            color: var(--text);
        }

        .brand-subtitle {
            font-size: 11px;
            color: var(--muted);
            margin-top: 3px;
        }

        .sidebar-label {
            color: var(--muted);
            font-size: 11px;
            letter-spacing: 1.3px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        [data-testid="stSidebar"] hr {
            border-color: var(--border);
            margin: 24px 0;
        }

        /* NAVEGACION */

        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 7px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            padding: 12px 14px;
            border-radius: 9px;
            transition: background .2s ease, box-shadow .2s ease;
            cursor: pointer;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: #1b2338;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: #261b38;
            box-shadow: inset 3px 0 0 var(--primary);
            font-weight: 650;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            display: none;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p {
            color: #e5efff;
        }

        /* ENCABEZADOS GENERALES */

        .page-header {
            margin-bottom: 30px;
        }

        .page-header h1 {
            margin-top: 5px;
            margin-bottom: 8px;
        }

        .page-header p {
            color: var(--muted);
            font-size: 15px;
            margin: 0;
        }

        .eyebrow {
            color: var(--primary);
            font-size: 11px;
            letter-spacing: 1.4px;
            font-weight: 750;
        }

        /* TARJETAS GENERALES */

        .card {
            background: linear-gradient(145deg, #171d32, #101727);
            border: 1px solid #35405b;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 6px 24px rgba(0,0,0,.20);
            transition:
                transform .25s ease,
                border-color .25s ease,
                box-shadow .25s ease;
        }

        .card:hover {
            transform: translateY(-3px);
            border-color: var(--primary);
            box-shadow:
                0 0 10px rgba(244,78,198,.20),
                0 0 24px rgba(244,78,198,.09);
        }

        .card h3 {
            margin-top: 0;
            color: var(--text);
        }

        .card p {
            line-height: 1.7;
            color: var(--muted);
        }

        /* METRICAS GENERALES */

        .metric-card {
            background: linear-gradient(145deg, #171d32, #101727);
            border: 1px solid #35405b;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 22px;
            box-shadow: 0 6px 24px rgba(0,0,0,.20);
            transition:
                transform .25s ease,
                border-color .25s ease,
                box-shadow .25s ease;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: var(--primary);
            box-shadow:
                0 0 10px rgba(244,78,198,.20),
                0 0 24px rgba(244,78,198,.09);
        }

        .metric-title {
            background: #211b36;
            padding: 18px 22px;
            border-bottom: 1px solid #514069;
            font-size: 14px;
            font-weight: 750;
            color: var(--text);
        }

        .metric-number {
            text-align: center;
            font-size: 65px;
            font-weight: 750;
            color: var(--secondary);
            padding-top: 25px;
            letter-spacing: -2px;
            text-shadow: 0 0 20px rgba(53,223,242,.20);
        }

        .metric-description {
            text-align: center;
            color: var(--muted);
            font-size: 13px;
            padding: 5px 15px 28px;
        }

        /* BOTONES GENERALES */

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 10px !important;
            min-height: 45px;
            font-weight: 650;
            transition:
                transform .2s ease,
                background .2s ease,
                box-shadow .2s ease,
                border-color .2s ease;
        }

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button,
        .stFormSubmitButton > button[kind="primary"] {
            background: linear-gradient(110deg, #a81780, #bd2c9e) !important;
            border: 1px solid var(--primary) !important;
            color: #fff !important;
            box-shadow: 0 0 10px rgba(244,78,198,.16);
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background: linear-gradient(110deg, #c51e95, #d43aaf) !important;
            border-color: #ff83dc !important;
            box-shadow:
                0 0 12px rgba(244,78,198,.38),
                0 0 28px rgba(244,78,198,.15) !important;
            transform: translateY(-2px);
        }

        .stButton > button[kind="secondary"] {
            background: #131d30;
            border: 1px solid #2ba8bc;
            color: #d5faff;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #172a3b;
            border-color: var(--secondary) !important;
            color: #fff;
            box-shadow: 0 0 14px rgba(53,223,242,.20) !important;
        }

        .stButton > button p,
        .stFormSubmitButton > button p {
            color: inherit !important;
        }

        /* ACTIVIDAD RECIENTE GENERAL */

        .recent-item {
            background: linear-gradient(145deg, #171d32, #101727);
            border: 1px solid #35405b;
            border-radius: 15px;
            padding: 14px 18px;
            margin-bottom: 9px;
            min-height: 75px;
            transition:
                transform .25s ease,
                border-color .25s ease,
                box-shadow .25s ease;
        }

        .recent-item:hover {
            transform: translateY(-3px);
            border-color: var(--primary);
            box-shadow:
                0 0 10px rgba(244,78,198,.20),
                0 0 24px rgba(244,78,198,.09);
        }

        .recent-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--text);
        }

        .recent-subtitle {
            font-size: 13px;
            color: var(--muted);
            margin-top: 4px;
        }

        /* FORMULARIOS */

        div[data-testid="stForm"] {
            background: linear-gradient(145deg, #151b30, #101726);
            border: 1px solid #483456;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 8px 30px rgba(0,0,0,.20);
            transition: border-color .2s ease;
        }

        div[data-testid="stForm"]:hover {
            border-color: #a0479c;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background: #0c1425;
            color: var(--text);
            border: 1px solid #3d4a68;
            border-radius: 8px;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: var(--secondary) !important;
            box-shadow: 0 0 0 1px rgba(53,223,242,.25) !important;
        }

        [data-baseweb="select"] > div {
            background: #0c1425;
            border-color: #3d4a68;
            border-radius: 8px;
            color: var(--text);
        }

        /* ARCHIVOS */

        [data-testid="stFileUploader"] {
            background: #121b2d;
            border: 2px dashed #366c80;
            border-radius: 14px;
            padding: 20px;
            transition: border-color .2s ease, box-shadow .2s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--secondary);
            box-shadow: 0 0 15px rgba(53,223,242,.12);
        }

        /* PESTANAS */

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            background: #151b30;
            border: 1px solid #35405b;
            border-radius: 8px;
            padding: 10px 22px;
            color: #c4d1e6;
        }

        .stTabs [aria-selected="true"] {
            background: #301c3e;
            color: #fff;
            border-color: var(--primary);
        }

        /* OTROS */

        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        hr {
            border: none;
            border-top: 1px solid var(--border);
        }

        .dashboard-footer {
            text-align: center;
            color: #8799b5;
            font-size: 12px;
            padding: 25px 0;
        }

        /* DASHBOARD: ENCABEZADO */

        .dashboard-hero {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 25px;
            min-height: 235px;
            padding: 35px 42px;
            border-radius: 22px;
            background: linear-gradient(
                115deg, #281431 0%, #151b35 58%, #0b2132 100%
            );
            border: 1px solid #503258;
            box-shadow: 0 15px 40px rgba(0,0,0,.18);
            overflow: hidden;
            margin-bottom: 18px;
        }

        .dashboard-hero-content {
            position: relative;
            z-index: 1;
            max-width: 680px;
        }

        .dashboard-eyebrow {
            color: #35dff2;
            font-size: 11px;
            font-weight: 750;
            letter-spacing: 1.5px;
        }

        .dashboard-hero h1 {
            font-size: clamp(29px, 3vw, 42px) !important;
            font-weight: 800 !important;
            margin: 13px 0 !important;
            line-height: 1.2;
            color: #fff !important;
            text-shadow: none !important;
        }

        .dashboard-hero h1 span:first-child {
            color: #f1f5ff !important;
        }

        .dashboard-hero h1 span:last-child {
            color: #f44ec6 !important;
        }

        .dashboard-hero p {
            font-size: 14px;
            color: #bdcbe1;
            line-height: 1.8;
            margin-bottom: 19px;
        }

        .dashboard-hero-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
        }

        .dashboard-hero-tags span {
            font-size: 11px;
            color: #c6d5ed;
            background: rgba(255,255,255,.055);
            border: 1px solid rgba(255,255,255,.10);
            padding: 7px 11px;
            border-radius: 30px;
        }

        .dashboard-hero-art {
            flex: 0 0 165px;
            display: flex;
            justify-content: center;
        }

        .dashboard-orbit {
            width: 155px;
            height: 155px;
            border: 1px solid rgba(53,223,242,.36);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 40px rgba(53,223,242,.08);
        }

        .dashboard-orbit-core {
            width: 100px;
            height: 100px;
            border-radius: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 850;
            color: white;
            background: linear-gradient(135deg, #bd278f, #236c9d);
            box-shadow: 0 0 30px rgba(244,78,198,.25);
            transform: rotate(-8deg);
        }

        /* DASHBOARD: SECCIONES */

        .dashboard-section-heading {
            margin: 12px 0 18px;
        }

        .dashboard-section-heading h2 {
            font-size: 21px !important;
            font-weight: 750 !important;
            margin: 0 0 5px !important;
        }

        .dashboard-section-heading p {
            font-size: 13px;
            color: #91a4bf;
            margin: 0;
        }

        .dashboard-tools-heading,
        .dashboard-bottom-heading {
            margin-top: 26px;
        }

        /* DASHBOARD: METRICAS */

        .dashboard-stat {
            min-height: 156px;
            padding: 20px 23px;
            background: linear-gradient(145deg, #171f34, #111827);
            border: 1px solid #35415c;
            border-radius: 16px;
            transition: border-color .2s ease, transform .2s ease;
        }

        .dashboard-stat:hover {
            border-color: #35dff2;
            transform: translateY(-2px);
        }

        .dashboard-stat-pink:hover {
            border-color: #f44ec6;
        }

        .dashboard-stat-top {
            display: flex;
            align-items: center;
            gap: 11px;
        }

        .dashboard-stat-icon {
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            font-size: 22px;
            color: #35dff2;
            background: rgba(53,223,242,.10);
        }

        .dashboard-stat-pink .dashboard-stat-icon {
            color: #f44ec6;
            background: rgba(244,78,198,.10);
        }

        .dashboard-stat-label {
            font-size: 13px;
            font-weight: 650;
            color: #e4ebfb;
        }

        .dashboard-stat-number {
            font-size: 36px;
            font-weight: 800;
            line-height: 1.3;
            color: #fff;
            margin-top: 10px;
        }

        .dashboard-stat-description {
            font-size: 12px;
            color: #91a4bf;
            margin-top: 3px;
        }

        /* DASHBOARD: HERRAMIENTAS */

        [class*="st-key-dashboard-tool-"] {
            background: linear-gradient(145deg, #171f34, #101827);
            border: 1px solid #35415c;
            border-radius: 17px;
            padding: 23px;
            min-height: 280px;
            transition: border-color .2s ease, transform .2s ease;
        }

        [class*="st-key-dashboard-tool-"]:hover {
            border-color: #f44ec6;
            transform: translateY(-2px);
        }

        .dashboard-tool-content {
            min-height: 188px;
        }

        .dashboard-tool-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 47px;
            height: 47px;
            border-radius: 13px;
            font-size: 25px;
            margin-bottom: 17px;
        }

        .dashboard-icon-cyan {
            background: rgba(53,223,242,.11);
            color: #35dff2;
        }

        .dashboard-icon-pink {
            background: rgba(244,78,198,.11);
            color: #f44ec6;
        }

        .dashboard-tool-tag {
            font-size: 10px;
            font-weight: 750;
            letter-spacing: 1px;
            color: #91a4bf;
            margin-bottom: 8px;
        }

        .dashboard-tool-content h3 {
            font-size: 18px !important;
            font-weight: 750 !important;
            margin: 0 0 10px !important;
        }

        .dashboard-tool-content p {
            font-size: 13px;
            line-height: 1.65;
            color: #a7b7cd;
            margin: 0;
        }

        [class*="st-key-dashboard-tool-"] .stButton button {
            width: 100%;
            min-height: 42px;
        }

        /* DASHBOARD: ACTIVIDAD Y ESPACIO DE TRABAJO */

        .st-key-dashboard-activity,
        .st-key-dashboard-workspace {
            background: linear-gradient(145deg, #171f34, #101827);
            border: 1px solid #35415c;
            border-radius: 17px;
            padding: 23px;
            min-height: 235px;
        }

        .st-key-dashboard-activity h4,
        .st-key-dashboard-workspace h4 {
            margin: 0 0 20px !important;
            font-size: 17px !important;
            color: #f1f5ff !important;
        }

        .dashboard-activity-item {
            display: flex;
            align-items: center;
            gap: 13px;
            border-bottom: 1px solid #303b56;
            padding: 13px 0;
        }

        .dashboard-activity-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            flex-shrink: 0;
            border-radius: 11px;
            background: rgba(53,223,242,.10);
            color: #35dff2;
        }

        .dashboard-activity-item strong {
            display: block;
            font-size: 13px;
            color: #f1f5ff;
            overflow-wrap: anywhere;
        }

        .dashboard-activity-item p {
            font-size: 12px;
            margin: 4px 0 0;
            color: #91a4bf;
        }

        .dashboard-empty {
            text-align: center;
            padding: 20px 8px;
        }

        .dashboard-empty span {
            display: block;
            font-size: 38px;
            color: #35dff2;
            margin-bottom: 10px;
        }

        .dashboard-empty strong {
            display: block;
            color: #e4ebfb;
            font-size: 14px;
        }

        .dashboard-empty p {
            font-size: 12px;
            margin-top: 7px;
            color: #91a4bf;
        }

        .dashboard-workspace-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding: 13px 0;
            border-bottom: 1px solid #303b56;
        }

        .dashboard-workspace-row:last-child {
            border-bottom: none;
        }

        .dashboard-workspace-row span {
            color: #91a4bf;
            font-size: 12px;
        }

        .dashboard-workspace-row strong {
            color: #f1f5ff;
            font-size: 13px;
            font-weight: 650;
            overflow-wrap: anywhere;
        }

        /* RESPONSIVE */

        @media (max-width: 900px) {
            .dashboard-hero {
                padding: 26px;
            }

            .dashboard-hero-art {
                display: none;
            }
        }

        @media (max-width: 768px) {
            .block-container {
                padding: 1.5rem 1rem;
            }

            .metric-number {
                font-size: 48px;
            }

            .card {
                padding: 18px;
            }
        }

        @media (max-width: 600px) {
            .dashboard-hero {
                padding: 22px;
            }

            .dashboard-stat {
                padding: 15px;
                min-height: 135px;
            }

            .dashboard-stat-number {
                font-size: 29px;
            }

            [class*="st-key-dashboard-tool-"] {
                min-height: auto;
            }

            .dashboard-tool-content {
                min-height: auto;
                margin-bottom: 20px;
            }
        }

        /* ACCESIBILIDAD */

        @media (prefers-reduced-motion: reduce) {
            .card,
            .metric-card,
            .recent-item,
            .dashboard-stat,
            [class*="st-key-dashboard-tool-"],
            .stButton > button,
            .stFormSubmitButton > button {
                transition: none !important;
            }

            .card:hover,
            .metric-card:hover,
            .recent-item:hover,
            .dashboard-stat:hover,
            [class*="st-key-dashboard-tool-"]:hover,
            .stButton > button:hover,
            .stFormSubmitButton > button:hover {
                transform: none !important;
            }
        }

/* CARGA DE DOCUMENTOS */

.carga-hero {
    background: linear-gradient(115deg, #281431, #151b35 58%, #0b2132);
    border: 1px solid #503258;
    border-radius: 22px;
    padding: 34px 40px;
    margin-bottom: 25px;
}

.carga-eyebrow {
    color: #35dff2;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.carga-hero h1 {
    font-size: clamp(29px, 3vw, 40px) !important;
    font-weight: 800 !important;
    margin: 0 0 12px !important;
    text-shadow: none !important;
}

.carga-hero h1 span:first-child {
    color: #f1f5ff !important;
}

.carga-hero h1 span:last-child {
    color: #f44ec6 !important;
}

.carga-hero p {
    color: #bdcbe1;
    font-size: 14px;
    line-height: 1.8;
    max-width: 700px;
    margin: 0;
}

.st-key-carga-formulario,
.st-key-carga-informacion {
    background: linear-gradient(145deg, #171f34, #101827);
    border: 1px solid #35415c;
    border-radius: 18px;
    padding: 25px;
    min-height: 365px;
}

.st-key-carga-formulario h3,
.st-key-carga-informacion h3 {
    font-size: 20px !important;
    margin: 0 0 10px !important;
    color: #f1f5ff !important;
}

.st-key-carga-formulario [data-testid="stFileUploader"] {
    background: #101b2d;
    border: 1px dashed #35a9bf;
    border-radius: 14px;
    padding: 15px;
}

.st-key-carga-formulario [data-testid="stFileUploader"]:hover {
    border-color: #35dff2;
    box-shadow: 0 0 18px rgba(53,223,242,.10);
}

.st-key-carga-formulario .stButton button {
    margin-top: 8px;
    min-height: 48px;
    font-weight: 750;
}

.carga-empty {
    min-height: 245px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
}

.carga-empty-icon {
    font-size: 48px;
    color: #35dff2;
    opacity: .75;
    margin-bottom: 18px;
}

.carga-empty strong {
    font-size: 15px;
    color: #f1f5ff;
}

.carga-empty p {
    font-size: 13px;
    color: #91a4bf;
    line-height: 1.7;
    max-width: 270px;
    margin-top: 10px;
}

.carga-file-info {
    text-align: center;
    padding: 20px 10px;
    border-bottom: 1px solid #303b56;
    margin-bottom: 10px;
}

.carga-file-icon {
    font-size: 44px;
    color: #35dff2;
    margin-bottom: 12px;
}

.carga-file-name {
    font-size: 15px;
    font-weight: 750;
    color: #f1f5ff;
    overflow-wrap: anywhere;
}

.carga-file-type {
    font-size: 12px;
    color: #91a4bf;
    margin-top: 6px;
}

.carga-detail-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 13px 0;
    border-bottom: 1px solid #303b56;
    font-size: 13px;
}

.carga-detail-row span {
    color: #91a4bf;
}

.carga-detail-row strong {
    color: #f1f5ff;
}

.carga-section-heading {
    margin: 35px 0 18px;
}

.carga-section-heading h2 {
    font-size: 21px !important;
    font-weight: 750 !important;
    margin: 0 0 7px !important;
}

.carga-section-heading p {
    color: #91a4bf;
    font-size: 13px;
    margin: 0;
}

.carga-document-card {
    display: flex;
    align-items: center;
    gap: 16px;
    background: linear-gradient(145deg, #171f34, #101827);
    border: 1px solid #35415c;
    border-radius: 15px;
    padding: 18px 22px;
    margin-bottom: 12px;
}

.carga-document-icon {
    width: 45px;
    height: 45px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: rgba(53,223,242,.10);
    color: #35dff2;
    font-size: 24px;
}

.carga-document-content {
    min-width: 0;
}

.carga-document-content strong {
    color: #f1f5ff;
    font-size: 14px;
    overflow-wrap: anywhere;
}

.carga-document-content p {
    color: #a7b7cd;
    font-size: 12px;
    margin: 5px 0;
    overflow-wrap: anywhere;
}

.carga-document-content span {
    color: #91a4bf;
    font-size: 12px;
}

.carga-history-empty {
    background: #111a2b;
    border: 1px dashed #35415c;
    border-radius: 15px;
    padding: 28px;
    text-align: center;
    color: #91a4bf;
    font-size: 13px;
}

@media (max-width: 768px) {
    .carga-hero {
        padding: 25px;
    }

    .st-key-carga-formulario,
    .st-key-carga-informacion {
        padding: 18px;
        min-height: auto;
    }

/* ==========================================================
   LIBRERIA DE CONTENIDOS - DARK TECH
   ESTILOS DE DESPLEGABLES Y MATERIALES
   ========================================================== */

[data-testid="stExpander"] {
    background: linear-gradient(145deg, #171f34, #101827);
    border: 1px solid #35415c !important;
    border-radius: 16px !important;
    margin-bottom: 14px;
    overflow: hidden;
    transition: border-color .2s ease, box-shadow .2s ease;
}

[data-testid="stExpander"]:hover {
    border-color: #f44ec6 !important;
    box-shadow: 0 0 18px rgba(244, 78, 198, .12);
}

[data-testid="stExpander"] summary {
    background: transparent;
    padding: 16px 20px;
    border-radius: 15px;
}

[data-testid="stExpander"] summary:hover {
    background: rgba(244, 78, 198, .05);
}

[data-testid="stExpander"] summary p {
    color: #f1f5ff !important;
    font-size: 15px;
    font-weight: 700;
}

[data-testid="stExpander"] summary svg {
    color: #35dff2;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #111a2c;
    border-top: 1px solid #303b56;
    padding: 18px 22px;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] p {
    color: #c4d1e6;
    line-height: 1.7;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] strong {
    color: #f1f5ff;
}

[data-testid="stExpander"] [data-testid="stDownloadButton"] button {
    background: #132538;
    border: 1px solid #35a9bf;
    border-radius: 10px;
    color: #d5faff;
    min-height: 45px;
    font-weight: 650;
}

[data-testid="stExpander"] [data-testid="stDownloadButton"] button:hover {
    background: #193448;
    border-color: #35dff2;
    color: #ffffff;
    box-shadow: 0 0 14px rgba(53, 223, 242, .18);
}
/* =========================================
   LIBRERIA - DISEÑO DARK TECH
   ========================================= */

[data-testid="stExpander"] {
    background: linear-gradient(145deg, #192239, #101827);
    border: 1px solid #35415c !important;
    border-radius: 18px !important;
    margin-bottom: 18px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0, 0, 0, .18);
    transition: border-color .25s ease, box-shadow .25s ease;
}

[data-testid="stExpander"]:hover {
    border-color: #f44ec6 !important;
    box-shadow: 0 0 22px rgba(244, 78, 198, .14);
}

[data-testid="stExpander"] summary {
    padding: 19px 24px;
    background: linear-gradient(
        110deg,
        rgba(244, 78, 198, .08),
        rgba(53, 223, 242, .035)
    );
}

[data-testid="stExpander"] summary p {
    color: #f1f5ff !important;
    font-size: 16px;
    font-weight: 750;
}

[data-testid="stExpander"] summary svg {
    color: #35dff2 !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #111a2c;
    border-top: 1px solid #303b56;
    padding: 24px;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] p {
    color: #b9c9e0;
    font-size: 14px;
    line-height: 1.8;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] strong {
    color: #f1f5ff;
}

/* VISUALIZAR MATERIAL */

[data-testid="stExpander"] .stButton button[kind="primary"] {
    background: linear-gradient(110deg, #a81780, #bd2c9e) !important;
    border: 1px solid #f44ec6 !important;
    color: #ffffff !important;
    border-radius: 11px !important;
    min-height: 48px;
    font-weight: 700;
    box-shadow: 0 0 12px rgba(244, 78, 198, .16);
}

[data-testid="stExpander"] .stButton button[kind="primary"]:hover {
    background: linear-gradient(110deg, #c51e95, #d43aaf) !important;
    box-shadow: 0 0 20px rgba(244, 78, 198, .35) !important;
    transform: translateY(-2px);
}

/* DESCARGAR JSON */

[data-testid="stExpander"] [data-testid="stDownloadButton"] button {
    background: #132538 !important;
    border: 1px solid #35a9bf !important;
    border-radius: 11px !important;
    color: #d5faff !important;
    min-height: 48px;
    font-weight: 700;
    transition: all .2s ease;
}

[data-testid="stExpander"] [data-testid="stDownloadButton"] button:hover {
    background: #193448 !important;
    border-color: #35dff2 !important;
    color: #ffffff !important;
    box-shadow: 0 0 18px rgba(53, 223, 242, .22);
    transform: translateY(-2px);
}

[data-testid="stExpander"] [data-testid="stDownloadButton"] button p {
    color: inherit !important;
}

/* MENSAJES INFORMATIVOS */

[data-testid="stAlert"] {
    background: #142239;
    border: 1px solid #356479;
    border-radius: 13px;
    color: #d5faff;
}

/* ADAPTACION A PANTALLAS PEQUEÑAS */

@media (max-width: 768px) {
    [data-testid="stExpander"] summary {
        padding: 15px;
    }

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        padding: 15px;
    }

    [data-testid="stExpander"] summary p {
        font-size: 14px;
    }
}

}

        </style>
        """,
        unsafe_allow_html=True
    )
