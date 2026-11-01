"""Streamlit UI over the HTTP API: `make ui`, once `make serve` is running.

It only talks to the API, so the same UI works against a local or a cloud URL:
ACTWISE_API_URL (default http://localhost:8000), plus ACTWISE_API_KEY when the API needs one.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
import streamlit as st
from dotenv import load_dotenv

from actwise.ingest.files import READERS

load_dotenv()  # .env fills in what the environment doesn't set
API_URL = os.environ.get("ACTWISE_API_URL") or "http://localhost:8000"
HEADERS = {"X-API-Key": key} if (key := os.environ.get("ACTWISE_API_KEY")) else {}
TIMEOUT = 60.0  # seconds: the API stops calling models after 50


def detail(response: httpx.Response) -> str:
    """The API's error message: FastAPI's `detail`, or the raw body."""
    try:
        found = response.json()["detail"]
    except (ValueError, KeyError, TypeError):
        return response.text
    if isinstance(found, list):  # input validation errors
        return "; ".join(str(error.get("msg")) for error in found)
    return str(found)


def call(path: str, **request: Any) -> dict[str, Any] | None:
    """POST to the API and return its JSON, or show the error and return None."""
    try:
        with st.spinner("Reading the law…"):
            response = httpx.post(f"{API_URL}{path}", headers=HEADERS, timeout=TIMEOUT, **request)
    except httpx.HTTPError as exc:
        st.error(f"The API at {API_URL} did not answer: {exc!r}")
        return None
    if response.is_error:
        st.error(f"Error {response.status_code}: {detail(response)}")
        return None
    return response.json()


def show_answer(reply: dict[str, Any]) -> None:
    """The answer, the notice, then each source under its label."""
    st.markdown(reply["answer"])
    st.caption(reply["disclaimer"])
    with st.expander(f"Sources ({len(reply['sources'])})"):
        for source in reply["sources"]:
            st.markdown(f"**{source['label']}** `[{source['id']}]`")
            st.text(source["text"])


def show_classification(result: dict[str, Any]) -> None:
    """The tier and confidence, the reasons, the citations and any follow-up questions."""
    st.subheader(result["tier"].replace("_", " ").capitalize())
    st.caption(f"Confidence {result['confidence']:.0%}. {result['disclaimer']}")
    st.markdown("\n".join(f"- {reason}" for reason in result["reasons"]))
    st.markdown("**Cited:** " + ", ".join(f"`{c}`" for c in result["citations"]))
    if result["follow_up_questions"]:
        st.markdown("**To decide, the classifier needs to know:**")
        st.markdown("\n".join(f"- {q}" for q in result["follow_up_questions"]))


st.set_page_config(page_title="ActWise", page_icon="⚖️")
st.title("ActWise")
st.caption("Cited answers on the EU AI Act and the GDPR, and an AI Act risk classifier.")
ask_tab, classify_tab = st.tabs(["Ask", "Classify"])

with ask_tab:
    with st.form("ask"):  # a form sends what was typed, even before the box loses focus
        lang = st.radio("Language", ["en", "fr"], format_func=str.upper, horizontal=True)
        question = st.text_input("Question", placeholder="Which AI practices are prohibited?")
        asked = st.form_submit_button("Ask")
    if asked and (reply := call("/ask", json={"question": question, "lang": lang})):
        show_answer(reply)

with classify_tab:
    with st.form("classify"):
        description = st.text_area("Describe the AI system", height=160)
        upload = st.file_uploader("Or upload a description", type=[s[1:] for s in READERS])
        submitted = st.form_submit_button("Classify")
    if submitted:
        if upload:
            result = call("/upload", files={"file": (upload.name, upload.getvalue())})
        else:
            result = call("/classify", json={"description": description})
        if result:
            show_classification(result)
