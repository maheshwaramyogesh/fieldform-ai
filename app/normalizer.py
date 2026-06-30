import json
import re
from datetime import date, datetime
from uuid import uuid4

from schema import InspectionReport, Severity, Status


def _normalize_date(value):
    """
    Normalize AI date formats into Python date objects.
    """

    if isinstance(value, date):
        return value

    if value is None:
        return date.today()

    value = str(value).strip()

    # Remove ordinal suffixes
    value = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", value)

    current_year = date.today().year

    formats = [
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%d %B %Y",
        "%B %d, %Y",
        "%d %b %Y",
        "%b %d, %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    # Handle dates without year
    formats_without_year = [
        "%d %B",
        "%B %d",
        "%d %b",
        "%b %d",
    ]

    for fmt in formats_without_year:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.replace(year=current_year).date()
        except ValueError:
            pass

    return date.today()


def _first_value(value, default):
    """Return first item if value is a list, otherwise return value or default."""
    if isinstance(value, list) and value:
        return value[0]
    if value in (None, "", "null"):
        return default
    return value


def _normalize_severity(value) -> Severity:
    """
    Return the highest severity found.
    """

    if not isinstance(value, list):
        value = [value]

    highest = Severity.LOW

    for item in value:
        key = str(item).strip().lower()

        if key == "high":
            return Severity.HIGH

        if key == "medium":
            highest = Severity.MEDIUM

    return highest


def _normalize_status(value) -> Status:
    status = str(_first_value(value, "Pending")).strip().lower()

    if status in ("resolved", "completed", "done"):
        return Status.RESOLVED
    if status in ("in progress", "progress", "ongoing"):
        return Status.IN_PROGRESS
    return Status.PENDING


def _normalize_issues(issues) -> list[str]:
    """
    Normalize issues from multiple AI output formats.
    """

    if not issues:
        return []

    # If AI returned JSON as a string
    if isinstance(issues, str):

        try:
            issues = json.loads(issues)

        except json.JSONDecodeError:
            return [issues]

    normalized = []

    if not isinstance(issues, list):
        return normalized

    for issue in issues:

        # Simple string
        if isinstance(issue, str):
            cleaned = re.sub(r"^Pending\s*-\s*", "", issue, flags=re.IGNORECASE)
            normalized.append(cleaned)
            continue

        # Dictionary
        if isinstance(issue, dict):

            if issue.get("description"):
                normalized.append(issue["description"])
                continue

            if issue.get("details"):
                normalized.append(issue["details"])
                continue

            if issue.get("issue"):
                normalized.append(issue["issue"])
                continue

            if issue.get("issue_type"):
                normalized.append(issue["issue_type"])
                continue

        # List format
        if isinstance(issue, list):

            if len(issue) >= 3:
                normalized.append(str(issue[2]))
                continue

            if len(issue) >= 1:
                normalized.append(str(issue[0]))

    return normalized


def _normalize_actions(actions) -> list[str]:

    if isinstance(actions, str):

        try:
            actions = json.loads(actions)
        except json.JSONDecodeError:
            return [actions]

    if isinstance(actions, list):
        return [str(action) for action in actions if action]

    return []


def _normalize_people_count(value) -> int:
    """
    Normalize people_count from different AI formats.
    """

    if value is None:
        return 0

    # Integer
    if isinstance(value, int):
        return value

    # Float
    if isinstance(value, float):
        return int(value)

    # Dictionary
    if isinstance(value, dict):

        if "total" in value:
            return int(value["total"])

        if "total_on_site" in value:
            return int(value["total_on_site"])

        workers = int(value.get("workers", 0))
        supervisors = int(value.get("supervisors", 0))

        return workers + supervisors

    # String
    if isinstance(value, str):

        numbers = re.findall(r"\d+", value)

        if numbers:
            return int(numbers[0])

    return 0


def _normalize_report_id(value) -> str:
    """
    Validate or generate a report ID.
    """
    if value is None:
        return f"REP-{uuid4().hex[:8].upper()}"

    value = str(value).strip()

    invalid_values = {
        "",
        "pending",
        "high",
        "medium",
        "low",
        "resolved",
        "in progress",
        "null",
        "none",
    }

    if value.lower() in invalid_values:
        return f"REP-{uuid4().hex[:8].upper()}"

    return value


def _normalize_confidence(value) -> float:
    """
    Normalize confidence score into a float between 0.0 and 1.0.
    Supports:
    97
    "97"
    "97%"
    0.97
    """

    if value is None:
        return 0.8

    if isinstance(value, str):
        value = value.strip().replace("%", "")

    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.8

    # Convert percentages to decimal
    if score > 1:
        score = score / 100

    # Clamp to valid range
    score = max(0.0, min(score, 1.0))

    return round(score, 2)


def _normalize_text(value, default="Unknown"):
    """
    Normalize text fields by replacing empty or invalid values.
    """

    if value is None:
        return default

    value = str(value).strip()

    if value == "":
        return default

    invalid_values = {
        "null",
        "none",
        "pending",
        "high",
        "medium",
        "low",
        "unknown",
        "n/a",
        "na",
    }

    if value.lower() in invalid_values:
        return default

    return value


def normalize_ai_output(ai_output: dict) -> InspectionReport:
    """Convert raw AI JSON into a valid InspectionReport."""

    return InspectionReport(
        report_id=_normalize_report_id(ai_output.get("report_id")),
        inspection_date=_normalize_date(ai_output.get("inspection_date")),
        state=_normalize_text(ai_output.get("state")),
        district=_normalize_text(ai_output.get("district")),
        location=_normalize_text(ai_output.get("location")),
        institution_name=_normalize_text(ai_output.get("institution_name")),
        institution_type=_normalize_text(ai_output.get("institution_type")),
        inspector_name=_normalize_text(ai_output.get("inspector_name")),
        summary=ai_output.get("summary") or "",
        people_count=_normalize_people_count(ai_output.get("people_count")),
        issues=_normalize_issues(ai_output.get("issues", [])),
        severity=_normalize_severity(ai_output.get("severity")),
        recommended_actions=_normalize_actions(
            ai_output.get("recommended_actions", [])
        ),
        status=_normalize_status(ai_output.get("status")),
        confidence_score=_normalize_confidence(ai_output.get("confidence_score")),
    )
