import os
from datetime import date

from app.database import create_database, save_report, get_all_reports, get_report_by_id
from app.schema import InspectionReport, Severity, Status

if os.path.exists("fieldform.db"):
    os.remove("fieldform.db")

create_database()

report = InspectionReport(
    report_id="REP-002",
    inspection_date=date.today(),
    state="Telangana",
    district="Hyderabad",
    location="Secunderabad",
    institution_name="Government High School",
    institution_type="School",
    inspector_name="Yogesh",
    summary="Roof leakage observed.",
    people_count=150,
    issues=[
        "Roof leakage",
        "No drinking water"
    ],
    severity=Severity.HIGH,
    recommended_actions=[
        "Repair roof",
        "Restore water supply"
    ],
    status=Status.PENDING,
    confidence_score=0.95
)

save_report(report)
reports = get_all_reports()

print("\nStored Reports:\n")

for stored_report in reports:
    print(stored_report)
    print("\nSingle Report:\n")

single_report = get_report_by_id(report.report_id)

print(single_report)
