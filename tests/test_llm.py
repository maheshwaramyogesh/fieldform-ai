import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.llm import clean_model_response, generate_report

def test_clean_model_response_removes_markdown_fence():
    response = """```json
{"location": "Government School"}
```"""

    cleaned = clean_model_response(response)

    assert cleaned == '{"location": "Government School"}'


@patch("app.llm.ollama.chat")
def test_generate_report_valid_json(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": '{"location": "Government School", "severity": "High"}'
        }
    }

    result = generate_report("Visited Government School. Roof leaking.")

    assert result["location"] == "Government School"
    assert result["severity"] == "High"


@patch("app.llm.ollama.chat")
def test_generate_report_markdown_json(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": """```json
{"location": "PHC Hospital", "severity": "Medium"}
```"""
        }
    }

    result = generate_report("Visited PHC Hospital.")

    assert result["location"] == "PHC Hospital"
    assert result["severity"] == "Medium"


@patch("app.llm.ollama.chat")
def test_generate_report_invalid_json(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": "{ invalid json }"
        }
    }

    result = generate_report("Bad response test")

    assert result["error"] == "Model did not return valid JSON."
    assert result["raw_response"] == "{ invalid json }"