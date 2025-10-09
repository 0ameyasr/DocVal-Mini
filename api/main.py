"""Main backend API setup using FastAPI."""

# --- Dependencies ---
import os
import google.generativeai as genai

from dotenv import load_dotenv
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# --- Cross-Module Imports ---
from extractor import extract_data
from validator import validate_data

from models import (
    DocumentRequest,
    ExtractedData,
    ValidationResponse,
)

# --- Model Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- FastAPI App Setup ---
app = FastAPI(
    title="Insurance Document Validator (Mini)",
    description="An API to validate extracted data from insurance documents using AI.",
    version="1.0.0",
)


# --- Status ---
@app.get("/")
async def status() -> JSONResponse:
    """
    Indicates if the service is running and available.
    """
    return JSONResponse({"status": "Service is up and running."}, status_code=200)


# --- API Endpoint ---
@app.post("/validate", response_model=ValidationResponse)
async def validate_document(request: DocumentRequest) -> ValidationResponse:
    """
    Validates an insurance document by extracting data via Gemini AI and running business rules.
    """
    extracted_data = None

    if not request.document_text or not request.document_text.strip():
        raise HTTPException(
            status_code=400, detail="Document text to be validated must not be empty."
        )

    # --- Extract Data ---
    raw_extracted_data = None
    try:
        raw_extracted_data = await extract_data(request.document_text)
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"AI service failed: {str(error)}"
        ) from error

    if not raw_extracted_data:
        raise HTTPException(
            status_code=502, detail="No data was returned from the extraction service."
        )

    # --- Parse & Validate ---
    try:
        extracted_data = ExtractedData(**raw_extracted_data)
    except ValidationError as error:
        raise HTTPException(
            status_code=422,
            detail=f"Extraction output schema validation failed: {error}",
        ) from error

    # --- Validation ---
    validation = None
    try:
        validation = await validate_data(extracted_data)
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Validation logic failed: {str(error)}"
        ) from error

    if not validation:
        raise HTTPException(
            status_code=502, detail="Validation returned an empty or invalid response."
        )

    # --- Final Response ---
    try:
        return ValidationResponse(
            extracted_data=extracted_data, validation_results=validation
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to construct validation response {str(error)}",
        ) from error
