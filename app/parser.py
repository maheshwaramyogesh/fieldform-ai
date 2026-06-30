import json
import re
from typing import Any


def clean_json_response(response: str) -> str:
    """
    Remove Markdown code fences from AI responses.
    """
    response = response.strip()

    response = re.sub(r"^```json\s*", "", response)
    response = re.sub(r"^```\s*", "", response)
    response = re.sub(r"\s*```$", "", response)

    return response.strip()


def parse_ai_response(response: str) -> dict[str, Any]:
    """
    Convert AI response into a Python dictionary.
    """

    cleaned = clean_json_response(response)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON returned by AI: {exc}") from exc
