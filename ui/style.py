import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #fbf9fb;
            --text: #24252a;
            --muted: #74808a;
            --card: #ffffff;
            --rose: #ffd0d2;
            --pink: #f7b0be;
            --mauve: #c5a6b9;
            --lavender: #a094ad;
            --slate: #748496;
            --blue: #a6bed0;
            --purple: #665970;
            --purple-hover: #51465b;
            --border: rgba(116, 132, 150, 0.2);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 920px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, span, div {
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        .hero-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-top: 4px solid var(--rose);
            border-radius: 24px;
            padding: 1.4rem;
            box-shadow: 0 18px 42px rgba(17, 24, 39, 0.08);
            margin-bottom: 1rem;
        }

        .soft-card {
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 12px 26px rgba(17, 24, 39, 0.06);
        }

        .white-card { background: #ffffff; }
        .lavender-card { background: #eeeaf0; }
        .mauve-card { background: #eadde5; }
        .blue-card { background: var(--blue); }
        .pink-card { background: #fbe5e9; }

        .muted {
            color: var(--muted) !important;
            font-size: 0.9rem;
        }

        .pill {
            display: inline-block;
            background: var(--purple);
            color: #ffffff !important;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-right: 0.4rem;
        }

        .stButton > button {
            background: var(--purple) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            padding: 0.65rem 1rem !important;
        }

        .stButton > button * {
            color: #ffffff !important;
        }

        .stButton > button:hover {
            background: var(--purple-hover) !important;
            color: #ffffff !important;
        }

        .stTextArea textarea,
        .stTextInput input {
            background: #ffffff !important;
            color: var(--text) !important;
            caret-color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
        }

        [data-testid="stDateInput"] input {
            background: #ffffff !important;
            color: #111111 !important;
            caret-color: #111111 !important;
        }

        [data-testid="stDateInput"] button,
        [data-testid="stDateInput"] button * {
            color: #111111 !important;
        }

        [data-baseweb="calendar"],
        [data-baseweb="calendar"] * {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        [data-baseweb="calendar"] button:hover {
            background-color: #fbe5e9 !important;
        }

        [data-baseweb="calendar"] button[aria-pressed="true"] {
            background-color: var(--rose) !important;
            color: #111111 !important;
        }

        .stTextArea textarea::placeholder,
        .stTextInput input::placeholder {
            color: #9ca3af !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{title}</h1>
            <p class="muted">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str | None, body: str | None, meta: str = "", variant: str = "white-card"):
    st.markdown(
        f"""
        <div class="soft-card {variant}">
            <div class="muted">{meta}</div>
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
