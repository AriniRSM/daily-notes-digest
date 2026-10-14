import streamlit as st

from ui.style import hero, card


def render():
    hero(
        "Ask Me",
        "Ask questions from your saved notes after RAG is connected.",
    )

    question = st.text_input(
        "Question",
        placeholder="What did I save about pgvector?",
    )

    if st.button("Ask", use_container_width=True):
        if not question.strip():
            st.warning("Ask a question first.")
        else:
            st.info("RAG API is not connected yet.")

    st.subheader("Answer")
    card(
        "I don’t know from your saved notes.",
        "Once retrieval is connected, answers will appear here with sources.",
        variant="white-card",
    )

    st.subheader("Sources")
    card("No sources yet", "Retrieved note and link sources will appear here.", variant="lavender-card")

    with st.expander("Retrieved snippets"):
        st.caption("Retrieved chunks will appear here.")