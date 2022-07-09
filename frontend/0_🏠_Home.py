import streamlit as st


st.set_page_config(
    page_title="PAPERLENS 0.0.1",
    page_icon="👋",
)

st.write("# Welcome to Paperlens 📑")

st.markdown(
    """
    Paperlens is a free, open-source application that helps you create and store documents for later retrieval:

    Basic features:

    - Full-text search
    - Semantic search for synonymous sentences
    - Group documents by tags

    Supported types of document:

    - ArXiv paper
    - Static website
    - Handin (also known as a self-written note)
    """
)
