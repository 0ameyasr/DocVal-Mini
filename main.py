# --- Dependencies ---

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from datetime import date

# --- Configuration ---

# Use environment variables for API key management
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# App Setup
app = FastAPI(
    title="Mini Insurance Document Validator",
    description="An API to validate extracted data from insurance documents using AI.",
    version="1.0.0"
)

# --- Pydantic Models ---

class DocumentRequest(BaseModel):
    """Request model for the document text."""
    document_text: str = Field(..., description="The raw text content of the insurance document.")

class ExtractedData(BaseModel):
    """Model for the data extracted by the AI service."""
    policy_number: Optional[str] = None
    vessel_name: Optional[str] = None
    policy_start_date: Optional[date] = None
    policy_end_date: Optional[date] = None
    insured_value: Optional[int] = None

class ValidationResult(BaseModel):
    """Model for a single validation check result."""
    rule: str
    status: str # "PASS" or "FAIL"
    message: str

class ValidationResponse(BaseModel):
    """The final response model for the /validate endpoint."""
    extracted_data: ExtractedData
    validation_results: List[ValidationResult]

# --- AI Extraction Logic ---

# TODO: Move this to its own module (e.g., ai_extractor.py) for bonus points.
async def extract_data_with_ai(document_text: str) -> Dict[str, Any]:
    """
    Uses a generative AI model to extract structured data from document text.
    """
    # This is where you will implement your prompt engineering and call to the Gemini API.
    # 1. Craft a detailed prompt.
    # 2. Configure the model to use JSON mode.
    # 3. Make the API call.
    # 4. Handle potential errors from the API.
    # 5. Return the extracted data as a dictionary.
    
    # Placeholder: Replace with your actual Gemini API call
    print("AI extraction not implemented. Returning placeholder data.")
    return {
        "policy_number": "PN-12345",
        "vessel_name": "MV Neptune",
        "policy_start_date": "2025-01-01",
        "policy_end_date": "2026-01-01",
        "insured_value": 1000000
    }

# --- API Endpoint ---

@app.post("/validate", response_model=ValidationResponse)
async def validate_document(request: DocumentRequest):
    """
    Validates an insurance document by extracting data via AI and running business rules.
    """
    # 1. Call the AI service to extract data from the document text
    try:
        raw_extracted_data = await extract_data_with_ai(request.document_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service failed: {str(e)}")

    # 2. Parse and validate the AI's output using your Pydantic model.
    try:
        extracted_data = ExtractedData(**raw_extracted_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"AI output did not match expected schema: {e}"
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
            message="Validation logic not implemented yet."
        )
    )

    # 4. Return the final, structured response.
    return ValidationResponse(
        extracted_data=extracted_data,
        validation_results=validation_results
    )