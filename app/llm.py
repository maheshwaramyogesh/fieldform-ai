import json
import re

import ollama

from prompts import SYSTEM_PROMPT, build_extraction_prompt


def clean_model_response(content: str) -> str:
    """Remove markdown fences and extract JSON text."""
    content = content.strip()
    content = re.sub(r"^```json\s*", "", content)
    content = re.sub(r"^```\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    return content.strip()


def generate_report(notes: str):
    """Generate a structured inspection report using a local Ollama model."""
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_extraction_prompt(notes)},
        ],
    )

    content = response["message"]["content"]
    cleaned_content = clean_model_response(content)

    try:
        return json.loads(cleaned_content)
    except json.JSONDecodeError:
        return {
            "error": "Model did not return valid JSON.",
            "raw_response": content,
        }
