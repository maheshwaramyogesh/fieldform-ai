SYSTEM_PROMPT = """
You are FieldForm AI, an offline assistant that converts field inspection notes
into structured JSON.

Rules:
- Return only valid JSON.
- Do not include markdown.
- Do not include explanations.
- Use the exact schema fields requested.
- If information is missing, use an empty string, empty list, 0, or "Pending".
"""


def build_extraction_prompt(notes: str) -> str:
    """Build a prompt for extracting structured inspection data."""

    return f"""
Convert the following field inspection notes into structured JSON.

Required JSON fields:
- report_id
- inspection_date
- state
- district
- location
- institution_name
- institution_type
- inspector_name
- summary
- people_count
- issues
- severity
- status
- confidence_score

Allowed severity values:
- Low
- Medium
- High

Allowed status values:
- Pending
- In Progress
- Resolved

Inspection Notes:
{notes}
"""
