# --- Dependencies ---
import os
import json

from google import genai
from typing import Dict, Any, Optional

# --- Cross-Module Imports ---
from models import ExtractedData

# --- Constants ---
GEMINI_MODEL_NAME = "gemini-2.0-flash"


# --- Prompt Fetcher ---
async def get_primer(path: str = "api/prompts/doc_extractor.txt") -> Optional[str]:
    if os.path.isfile(path):
        with open(path, "r") as context:
            return context.read()
    else:
        return None


# -- Extraction Logic --
async def extract_data(document_text: str) -> Dict[str, Any]:
    """
    Uses a generative AI model to extract structured data from document text.
    """

    # --- Load Decorated Prompt Primer ---
    primer = await get_primer()
    decorated_primer = primer.format(document_text)

    # --- Configure Extractor Model ---
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
