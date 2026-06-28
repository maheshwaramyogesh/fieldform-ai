import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.parser import parse_ai_response


def test_parse_plain_json():
    response = """
    {
        "location": "Government School",
        "people_count": 150,
        "severity": "High"
    }
    """

    result = parse_ai_response(response)

    assert result["location"] == "Government School"
    assert result["people_count"] == 150
    assert result["severity"] == "High"


def test_parse_markdown_json():
    response = """
    ```json
    {
        "location": "PHC Hospital",
        "people_count": 75,
        "severity": "Medium"
    }
    ```
    """

    result = parse_ai_response(response)

    assert result["location"] == "PHC Hospital"
    assert result["people_count"] == 75
    assert result["severity"] == "Medium"


def test_invalid_json():
    response = "{ invalid json }"

    with pytest.raises(ValueError):
        parse_ai_response(response)