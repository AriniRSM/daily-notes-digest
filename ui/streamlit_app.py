import streamlit as st

from ui.screens import ask_me, digest, inbox
from ui.style import apply_theme


st.set_page_config(
    page_title="Daily Notes Digest",
    page_icon="DN",
    layout="wide",
)

apply_theme()

st.sidebar.title("Daily Notes")

screen = st.sidebar.radio(
    "Navigation",
    ["Inbox", "Digest", "Ask Me"],
    label_visibility="collapsed",
)

if screen == "Inbox":
    inbox.render()
elif screen == "Digest":
    digest.render()
else:
    ask_me.render()