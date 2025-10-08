# --- Dependencies ---
import os
import google.generativeai as genai

from dotenv import load_dotenv
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException

# --- Cross-Module Imports ---
from extractor import extract_data
from validator import validate_data

from models import (
    DocumentRequest,
    ExtractedData,
    ValidationResponse,
)

# --- Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# FastAPI App Setup
app = FastAPI(
    title="Mini Insurance Document Validator",
    description="An API to validate extracted data from insurance documents using AI.",
    version="1.0.0",
)


# --- API Endpoint ---
@app.post("/validate", response_model=ValidationResponse)
async def validate_document(request: DocumentRequest):
    """
    Validates an insurance document by extracting data via AI and running business rules.
    """
    extracted_data = None

    # 1. Call the AI service to extract data from the document text
    try:
        raw_extracted_data = await extract_data(request.document_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service failed: {str(e)}")

    # 2. Parse and validate the AI's output using your Pydantic model
    try:
        extracted_data = ExtractedData(**raw_extracted_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=400, detail=f"AI output did not match expected schema: {e}"
        )

    # 3. Validation logic
    if extracted_data:
        try:
            validation = await validate_data(extracted_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI service failed: {str(e)}")

    # 4. Return the final, structured response.
    validation_response = None
    try:
        validation_response = ValidationResponse(
            extracted_data=extracted_data, validation_results=validation
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"AI output did not match expected schema: {e}"
        )

    return validation_response