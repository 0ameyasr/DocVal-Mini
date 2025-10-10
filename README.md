# Insurance Document Validator

An AI-powered API service that extracts and validates data from marine insurance documents using Google's Gemini AI.

## Features

- **AI Extraction**: Automatically extracts policy details using Gemini 2.0 Flash
- **Business Rule Validation**: Validates extracted data against predefined rules
- **FastAPI Backend**: RESTful API with automatic documentation
- **Streamlit Demo**: Interactive web interface for testing

## Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. Clone the repository and navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Running the API

Start the FastAPI server:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

- **Swagger docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Running the Demo App

Launch the Streamlit interface:
```bash
streamlit run api/demo.py
```

## API Usage

### Validate Document

**Endpoint**: `POST /validate`

**Request Body**:
```json
{
  "document_text": "Your insurance document text here..."
}
```

**Response**:
```json
{
  "extracted_data": {
    "policy_number": "HM-2025-10-A4B",
    "vessel_name": "MV Neptune",
    "policy_start_date": "2025-11-01",
    "policy_end_date": "2026-10-31",
    "insured_value": 5000000
  },
  "validation_results": [
    {
      "rule": "Completeness Check",
      "status": "PASS",
      "message": "Policy number is present."
    }
  ]
}
```

## Validation Rules

1. **Completeness Check**: Policy number must be present
2. **Date Consistency**: End date must be after start date
3. **Vessel Name Match**: Vessel must be on approved list
4. **Value Check**: Insured value must be positive

## Project Structure

```
api/
├── main.py              # FastAPI application
├── core.py              # Core validation logic
├── demo.py              # Streamlit demo app
├── extractor.py         # AI extraction module
├── validator.py         # Business rule validation
├── models.py            # Pydantic data models
├── prompts/
│   └── doc_extractor.txt  # AI prompt template
└── assets/
    ├── valid_vessels.json      # Approved vessel list
    ├── sample_document_pass.txt
    └── sample_document_fail.txt
```

## Testing

Sample documents are provided in `api/assets/`:
- `sample_document_pass.txt` - Valid document
- `sample_document_fail.txt` - Invalid document with errors

## License

Apache License 2.0

## Tech Stack

- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Google Gemini AI** - Document extraction
- **Streamlit** - Demo interface
- **Uvicorn** - ASGI server
