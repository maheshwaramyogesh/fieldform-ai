from app.normalizer import normalize_ai_output


sample_ai_output = {
    "report_id": None,
    "inspection_date": None,
    "state": "null",
    "district": "null",
    "location": "Government High School",
    "institution_name": "Government High School",
    "institution_type": "School",
    "inspector_name": "null",
    "summary": "Roof leaking in Block A. No drinking water. Needs urgent repair.",
    "people_count": "150",
    "issues": [
        {
            "issue_type": "Roof Leaking",
            "description": "Roof leaking in Block A."
        },
        {
            "issue_type": "No Drinking Water",
            "description": "No drinking water."
        }
    ],
    "severity": ["High"],
    "status": ["Pending"],
    "confidence_score": None
}


report = normalize_ai_output(sample_ai_output)

print(report.model_dump_json(indent=2))