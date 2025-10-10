"""Core integrated document validation logic for an standalone Streamlit app"""

# --- Dependencies ---
from extractor import extract_data
from validator import validate_data
from models import ExtractedData, ValidationResponse


async def validate_document_logic(document_text: str) -> ValidationResponse:
    if not document_text.strip():
        raise ValueError("Document text cannot be empty")

    # Extract data
    raw_extracted_data = await extract_data(document_text)
    if not raw_extracted_data:
        raise ValueError("No data returned from extraction")

    # Validate schema
    extracted_data = ExtractedData(**raw_extracted_data)

    # Run validations
    validation_results = await validate_data(extracted_data)

    return ValidationResponse(
        extracted_data=extracted_data, validation_results=validation_results
    )
