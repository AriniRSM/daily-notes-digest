from html import escape

import streamlit as st

from ui.api_client import create_item, list_items
from ui.style import hero


def _save_inbox_item():
    raw_input = st.session_state.get("inbox_raw_input", "").strip()
    if not raw_input:
        st.session_state["inbox_feedback"] = ("warning", "Add something before saving.")
        return

    try:
        create_item(raw_input)
        st.session_state["inbox_raw_input"] = ""
        st.session_state["inbox_feedback"] = ("success", "Saved.")
    except Exception as error:
        message = str(error)
        if "already saved" in message.lower():
            st.session_state["inbox_feedback"] = ("warning", message)
        else:
            st.session_state["inbox_feedback"] = ("error", f"Could not save item: {message}")


def render():
    hero(
        "Daily Notes Digest",
        "An intentional dumping space for all your notes and thoughts , copy+paste on the go to revisit anytime!",
    )

    raw_input = st.text_area(
        "Share your thoughts...",
        placeholder="Paste a link, copied text, newsletter snippet, quote, or typed note...",
        height=170,
        key="inbox_raw_input",
    )

    st.button(
        "Save",
        use_container_width=True,
        on_click=_save_inbox_item,
    )

    feedback = st.session_state.pop("inbox_feedback", None)
    if feedback:
        level, message = feedback
        getattr(st, level)(message)

    st.subheader("Today's Dumps")

    try:
        items = list_items()
    except Exception as error:
        st.error(f"Could not load items: {error}")
        items = []

    if not items:
        st.caption("Nothing saved yet today.")

    variants = ["white-card", "lavender-card", "blue-card", "pink-card"]

    for index, item in enumerate(items):
        preview = item["raw_input"]
        if len(preview) > 180:
            preview = preview[:180] + "..."

        preview = escape(preview)
        item_type = escape(item["item_type"])
        status = escape(item["status"])
        variant = variants[index % len(variants)]

        st.markdown(
            f"""
            <div class="soft-card {variant}">
                <div>
                    <span class="pill">{item_type}</span>
                    <span class="muted">{status}</span>
                </div>
                <p style="margin-top: 0.8rem; font-weight: 650;">{preview}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
