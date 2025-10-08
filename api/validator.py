import json

from typing import List
from pathlib import Path
from datetime import date
from models import ExtractedData, ValidationResult

API_DIR = Path(__file__).parent

with open(API_DIR / "assets" / "valid_vessels.json", 'r') as file:
    VALID_VESSELS = json.load(file)

async def validate_data(extracted_data: ExtractedData) -> List[ValidationResult]:
    results = []

    # 1, Completeness Check
    if not extracted_data.policy_number:
        results.append(ValidationResult(
            rule="Completeness Check",
            status="FAIL",
            message="Policy number is missing."
        ))
    else:
        results.append(ValidationResult(
            rule="Completeness Check",
            status="PASS",
            message="Policy number is present."
        ))

    # 2, Date Consistency
    if (extracted_data.policy_start_date and extracted_data.policy_end_date
            and extracted_data.policy_start_date > extracted_data.policy_end_date):
        results.append(ValidationResult(
            rule="Date Consistency",
            status="FAIL",
            message="Policy end date cannot be before the start date."
        ))
    else:
        results.append(ValidationResult(
            rule="Date Consistency",
            status="PASS",
            message="Policy end date is after start date."
        ))

    # 3, Vessel Name Match
    if extracted_data.vessel_name not in VALID_VESSELS:
        results.append(ValidationResult(
            rule="Vessel Name Match",
            status="FAIL",
            message=f"Vessel '{extracted_data.vessel_name}' is not on the approved list."
        ))
    else:
        results.append(ValidationResult(
            rule="Vessel Name Match",
            status="PASS",
            message=f"Vessel '{extracted_data.vessel_name}' is on the approved list."
        ))

    # 4, Value Check
    if extracted_data.insured_value is None or extracted_data.insured_value <= 0:
        results.append(ValidationResult(
            rule="Value Check",
            status="FAIL",
            message="Insured value must be a positive number."
        ))
    else:
        results.append(ValidationResult(
            rule="Value Check",
            status="PASS",
            message="Insured value is valid."
        ))

    return results
