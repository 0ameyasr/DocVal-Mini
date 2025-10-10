"""Streamlit app for demonstration (integrated with API logic)"""

# --- Dependencies ---

import streamlit as st
import asyncio
from core import validate_document_logic

# --- App Setup ---

st.title("Insurance Document Validator")

document_text = st.text_area("Paste your insurance document text:")

if st.button("Validate"):
    if not document_text.strip():
        st.error("Document text cannot be empty")
    else:
        try:
            result = asyncio.run(validate_document_logic(document_text))
            st.success("Validation successful!")
            st.json(result.dict())
        except Exception as e:
            st.error(f"Validation failed: {e}")
