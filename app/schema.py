from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Status(StrEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"


class InspectionReport(BaseModel):
    report_id: str = Field(..., description="Unique report ID")

    inspection_date: date

    state: str

    district: str

    location: str

    institution_name: str

    institution_type: str

    inspector_name: str

    summary: str

    people_count: int = Field(..., ge=0)

    recommended_actions: list[str] = Field(
        description="Recommended actions to resolve the issues"
    )

    issues: list[str]

    severity: Severity

    status: Status = Status.PENDING

    confidence_score: float = Field(..., ge=0.0, le=1.0)
