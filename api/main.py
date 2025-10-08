# --- Dependencies ---

import os
import google.generativeai as genai

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# --- Cross-Module Imports ---

from api.extractor import extract_data
from api.models import (
    DocumentRequest,
    ExtractedData,
    ValidationError,
    ValidationResponse,
    ValidationResult,
)

# --- Configuration ---

# Use environment variables for API key management
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# App Setup
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
    # 1. Call the AI service to extract data from the document text
    try:
        raw_extracted_data = await extract_data(request.document_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service failed: {str(e)}")

    # 2. Parse and validate the AI's output using your Pydantic model.
    try:
        extracted_data = ExtractedData(**raw_extracted_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=400, detail=f"AI output did not match expected schema: {e}"
        )

    # 3. TODO: Implement your validation logic here.
    #    This part remains the same as the previous version of the assignment.
    #    - Load the valid vessel names from the JSON file.
    #    - Create a list to hold your ValidationResult objects.
    #    - Run each of the 4 required validation checks.
    #    - Append the result of each check to your list.

    validation_results = []

    # Placeholder for your logic
    validation_results.append(
        ValidationResult(
            rule="Placeholder",
            status="FAIL",
            message="Validation logic not implemented yet.",
        )
    )

    # 4. Return the final, structured response.
    return ValidationResponse(
        extracted_data=extracted_data, validation_results=validation_results
    )
