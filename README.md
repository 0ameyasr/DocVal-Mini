# DocVal-Mini

DocVal-Mini is an AI-powered Insurance Document Validator built with FastAPI and Google Gemini AI. This MVP automatically extracts and validates marine insurance policy data from unstructured document text.

## Overview

This tool processes insurance documents to extract key policy information and validates it against business rules. The system uses Google's Gemini AI for intelligent data extraction and applies rule-based validation to ensure data quality and compliance.

## Features

- **AI-Powered Extraction**: Leverages Gemini-2.0-Flash to extract structured data from unstructured document text
- **Automated Validation**: Applies four critical business rules to ensure data integrity
- **RESTful API**: Clean FastAPI interface for easy integration
- **Robust Error Handling**: Comprehensive validation and error responses
- **Type Safety**: Pydantic models throughout for data validation

## Architecture

```
api/
├── main.py           # FastAPI application and endpoint definitions
├── extractor.py      # Gemini AI integration for data extraction
├── validator.py      # Business rule validation logic
├── models.py         # Pydantic data models
├── prompts/
│   └── doc_extractor.txt  # AI extraction prompt template
└── assets/
    ├── valid_vessels.json          # Approved vessel registry
    ├── sample_document_pass.txt    # Example valid document
    └── sample_document_fail.txt    # Example invalid document
```

## Installation

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd DocVal-Mini
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the application:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Health Check

```bash
GET /
```

Returns service status.

### Validate Document

```bash
POST /validate
Content-Type: application/json

{
  "document_text": "*** OFFICIAL COVER NOTE - GLOBAL MARINE ASSURANCE ***\n\nPolicy ID: HM-2025-10-A4B\nVessel: MV Neptune\n..."
}
```

#### Response

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
    },
    {
      "rule": "Date Consistency",
      "status": "PASS",
      "message": "Policy end date is after start date."
    },
    {
      "rule": "Vessel Name Match",
      "status": "PASS",
      "message": "Vessel 'MV Neptune' is on the approved list."
    },
    {
      "rule": "Value Check",
      "status": "PASS",
      "message": "Insured value is valid."
    }
  ]
}
```

## Validation Rules

The system applies four critical validation rules:

1. **Completeness Check**: Ensures policy number is present
2. **Date Consistency**: Verifies policy end date is after start date
3. **Vessel Name Match**: Confirms vessel is on the approved list
4. **Value Check**: Validates insured value is positive

## Data Extraction

The AI extracts the following fields from document text:

- `policy_number`: Policy identifier or reference number
- `vessel_name`: Name of the insured marine vessel
- `policy_start_date`: Policy effective date
- `policy_end_date`: Policy expiration date
- `insured_value`: Total insured value in dollars

Fields that cannot be reliably extracted default to `null`.

## Testing

Sample documents are provided in `api/assets/`:

- `sample_document_pass.txt`: Valid document that passes all checks
- `sample_document_fail.txt`: Invalid document that fails multiple rules

Run tests with:
```bash
pytest
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security Features

The extraction prompt includes safeguards against:
- Prompt injection attacks
- Fake data generation requests
- Incoherent or manipulated input
- Role-playing instructions

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Development

### Code Formatting

Format code with Black:
```bash
black .
```

### Project Structure

- `main.py`: API routes and application setup
- `extractor.py`: AI-powered data extraction
- `validator.py`: Business rule validation
- `models.py`: Pydantic schemas for type safety
- `prompts/`: AI prompt templates
- `assets/`: Reference data and sample files