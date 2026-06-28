from datetime import date
from uuid import uuid4

from app.schema import InspectionReport, Severity, Status


def _first_value(value, default):
    """Return first item if value is a list, otherwise return value or default."""
    if isinstance(value, list) and value:
        return value[0]
    if value in (None, "", "null"):
        return default
    return value


def _normalize_severity(value) -> Severity:
    severity = str(_first_value(value, "Medium")).strip().lower()

    if severity == "high":
        return Severity.HIGH
    if severity == "low":
        return Severity.LOW
    return Severity.MEDIUM


def _normalize_status(value) -> Status:
    status = str(_first_value(value, "Pending")).strip().lower()

    if status in ("resolved", "completed", "done"):
        return Status.RESOLVED
    if status in ("in progress", "progress", "ongoing"):
        return Status.IN_PROGRESS
    return Status.PENDING


def _normalize_issues(issues) -> list[str]:
    normalized = []

    if not isinstance(issues, list):
        return normalized

    for issue in issues:
        if isinstance(issue, dict):
            description = issue.get("description") or issue.get("issue_type")
            if description:
                normalized.append(str(description))
        elif isinstance(issue, str):
            normalized.append(issue)

    return normalized


def _normalize_actions(actions) -> list[str]:
    if isinstance(actions, list):
        return [str(action) for action in actions if action]
    if isinstance(actions, str):
        return [actions]
    return []


def normalize_ai_output(ai_output: dict) -> InspectionReport:
    """Convert raw AI JSON into a valid InspectionReport."""

    return InspectionReport(
        report_id=ai_output.get("report_id") or f"REP-{uuid4().hex[:8].upper()}",
        inspection_date=ai_output.get("inspection_date") or date.today(),
        state=ai_output.get("state") if ai_output.get("state") not in (None, "null") else "Unknown",
        district=ai_output.get("district") if ai_output.get("district") not in (None, "null") else "Unknown",
        location=ai_output.get("location") or "Unknown",
        institution_name=ai_output.get("institution_name") or "Unknown",
        institution_type=ai_output.get("institution_type") or "Unknown",
        inspector_name=ai_output.get("inspector_name") if ai_output.get("inspector_name") not in (None, "null") else "Unknown",
        summary=ai_output.get("summary") or "",
        people_count=int(ai_output.get("people_count") or 0),
        issues=_normalize_issues(ai_output.get("issues", [])),
        severity=_normalize_severity(ai_output.get("severity")),
        recommended_actions=_normalize_actions(ai_output.get("recommended_actions", [])),
        status=_normalize_status(ai_output.get("status")),
        confidence_score=float(ai_output.get("confidence_score") or 0.8),
    )