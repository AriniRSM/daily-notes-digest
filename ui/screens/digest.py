import streamlit as st

from ui.api_client import generate_today_digest, get_digest_data
from ui.style import hero, card


def render():
    hero(
        "Digest",
        "Your personalized digest edition of all your random thoughts and useful notes",
    )

    selected_date = st.date_input("Digest date")

    if "latest_digest" not in st.session_state:
        try:
            st.session_state["latest_digest"] = get_digest_data()
        except Exception as error:
            st.warning(str(error))
            st.session_state["latest_digest"] = None

    if st.button("Generate Digest", use_container_width=True):
        try:
            with st.spinner("Generating digest..."):
                digest = generate_today_digest(selected_date)
                st.session_state["latest_digest"] = digest
            st.success("Digest generated.")
        except Exception as error:
            st.error(str(error))

    digest = st.session_state.get("latest_digest")
    if not digest:
        st.caption("Generate a digest to see today's summary.")
        return

    st.subheader(digest["title"])
    st.subheader("### Overview of Topics")

    overview_topics = digest.get("overview_topics", [])

    if not overview_topics:
        st.caption("No topics found.")
    else:
        for topic in overview_topics:
            card(
                title=topic,
                body="",
                meta="Topic",
                variant="lavender-card",
            )


    st.subheader("### Summaries")
    summaries = digest.get("summaries", [])
    if not summaries:
        st.caption("No summaries found.")
    else:
        for summary in summaries:
            title = summary.get("title", "Untitled")
            item_type = summary.get("item_type", "unknown")
            summary_text = summary.get("summary", "")
            content_preview = summary.get("content_preview", "")

            with st.expander(f"{title} · {item_type}", expanded=True):
                st.write(summary_text)

                if content_preview:
                    st.caption("Preview")
                    st.write(content_preview)


    st.markdown("### Links")
    links = digest.get("links", [])
    if not links:
        st.caption("No links saved today.")
    else:
        for link in links:
            title = link.get("title", "Link")
            source_url = link.get("source_url")
            if source_url:
                card(
                    title=title,
                    body=f'<a href="{source_url}" target="_blank">{source_url}</a>',
                    meta="Saved link",
                    variant="blue-card",
                )

    st.markdown("### Action Items")
    action_items = digest.get("action_items", [])
    if not action_items:
        st.caption("No action items generated yet.")
    else:
        for index, item in enumerate(action_items, start=1):
            card(
                title=f"Next Step {index}",
                body=item,
                meta="Suggested from today’s notes",
                variant="pink-card",
            )
