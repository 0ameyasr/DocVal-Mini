"""Extractor module that uses Gemini to extract data from document text"""

# --- Dependencies ---
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from google import genai

# --- Cross-Module Imports ---
from models import ExtractedData

# --- Constants ---
GEMINI_MODEL_NAME = "gemini-2.0-flash"
API_DIR = Path(__file__).parent


# --- Prompt Fetcher ---
async def get_primer(
    path: str = API_DIR / "prompts" / "doc_extractor.txt",
) -> Optional[str]:
    """
    Reads the primer file, robust to CWD location
    """
    if os.path.isfile(path):
        with open(path, mode="r", encoding="utf8") as context:
            return context.read()
    else:
        print(f"ERR: Prompt file not found at {path}")
        return None


# -- Extraction Logic --
async def extract_data(document_text: str) -> Dict[str, Any]:
    """
    Uses a generative AI model to extract structured data from document text.
    """

    # --- Load Decorated Prompt Primer ---
    decorated_primer = None
    primer = await get_primer()
    if primer:
        decorated_primer = primer.format(document_text)

    # --- Configure Extractor Model ---
    response_txt = None
    if decorated_primer:
        client = genai.Client()
        response_txt = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=decorated_primer,
            config={
                "response_mime_type": "application/json",
                "response_schema": ExtractedData,
            },
        ).text

    return json.loads(response_txt) if response_txt else None
