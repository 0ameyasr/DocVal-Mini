# --- Dependencies ---
import os
import json
from pathlib import Path
from google import genai
from typing import Dict, Optional, List

# --- Cross-Module Imports ---
from models import ExtractedData, ValidationResult

# --- Constants ---
GEMINI_MODEL_NAME = "gemini-2.0-flash"
API_DIR = Path(__file__).parent


# --- Prompt Fetcher ---
async def get_primer(
    path: str = API_DIR / "prompts" / "doc_validator.txt",
) -> Optional[str]:
    """
    Reads the primer file, robust to CWD location
    """
    if os.path.isfile(path):
        with open(path, "r") as context:
            return context.read()
    else:
        print(f"ERR: Prompt file not found at {path}")
        return None


# --- Fetch Valid Vessels ---
async def get_valid_vessels(
    path: str = "assets/valid_vessels.json",
) -> Optional[List[str]]:
    if os.path.isfile(path):
        return json.dumps(path)


# -- Extraction Logic --
async def validate_data(extracted_data: ExtractedData) -> List[Dict[str, str]]:
    """
    Uses a generative AI model to extract structured data from document text.
    """

    # --- Load Decorated Prompt Primer ---
    primer = await get_primer()
    valid_vessels = await get_valid_vessels()
    decorated_primer = primer.format(valid_vessels, extracted_data)

    # --- Configure Extractor Model ---
    client = genai.Client()
    response_txt = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=decorated_primer,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[ValidationResult],
        },
    ).text

    return json.loads(response_txt) if response_txt else None
