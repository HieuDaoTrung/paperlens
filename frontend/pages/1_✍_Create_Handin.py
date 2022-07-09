from pydantic import BaseModel
from datetime import date
import streamlit as st
from typing import List
import requests
from box import Box

cfg = Box.from_yaml(filename="./pages/config.yaml")

TAGS = ["scientific", "novel", "biography", "todo", "note"]


class HandIn(BaseModel):
    """Documents that are manually input by the user"""
    title: str
    author: str
    description: str
    content: str
    tags: List[str]
    publish_date: str


def create_HandIn(doc: HandIn):
    headers = {
        "Content-Type": "application/json"
    }

    payload = doc.json()
    response = requests.request(
        method="POST",
        url=cfg.DOCUMENT_MANAGER_TMP,
        headers=headers,
        data=payload
    )
    if response.status_code == 201:
        "Your handin is successfully created."


with st.form("Create handin", clear_on_submit=True):
    title = st.text_input("Title")
    author = st.text_input("Author")
    description = st.text_area("Description", max_chars=300)
    content = st.text_area("Content")
    tags = st.multiselect("Tags", options=TAGS)
    publish_date = date.today().strftime("%m/%d/%Y")

    doc = HandIn(
        title=title,
        author=author,
        description=description,
        content=content,
        tags=tags,
        publish_date=publish_date
    )

    create_is_clicked = st.form_submit_button("Create")

    if create_is_clicked:
        create_HandIn(doc)
