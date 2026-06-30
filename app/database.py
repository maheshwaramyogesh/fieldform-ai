import json
import sqlite3
from pathlib import Path

DATABASE_NAME = Path(__file__).resolve().parent / "fieldform.db"


def create_database():
    """Create the SQLite database and inspection_reports table."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspection_reports (
            report_id TEXT PRIMARY KEY,
            inspection_date TEXT,
            state TEXT,
            district TEXT,
            location TEXT,
            institution_name TEXT,
            institution_type TEXT,
            inspector_name TEXT,
            summary TEXT,
            people_count INTEGER,
            issues TEXT,
            severity TEXT,
            recommended_actions TEXT,
            status TEXT,
            confidence_score REAL
        )
    """)

    conn.commit()
    conn.close()


def save_report(report):
    """Save an inspection report to the database."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT OR REPLACE INTO inspection_reports VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """,
        (
            report.report_id,
            str(report.inspection_date),
            report.state,
            report.district,
            report.location,
            report.institution_name,
            report.institution_type,
            report.inspector_name,
            report.summary,
            report.people_count,
            json.dumps(report.issues),
            report.severity.value,
            json.dumps(report.recommended_actions),
            report.status.value,
            report.confidence_score,
        ),
    )

    conn.commit()
    conn.close()


def get_all_reports():
    """Retrieve all inspection reports."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inspection_reports")

    reports = cursor.fetchall()

    conn.close()

    return reports


def update_status(report_id, new_status):
    """Update the status field of a single report."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE inspection_reports SET status = ? WHERE report_id = ?",
        (new_status, report_id),
    )

    conn.commit()
    conn.close()


def delete_report(report_id):
    """Delete a single report by its ID."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM inspection_reports WHERE report_id = ?",
        (report_id,),
    )

    conn.commit()
    conn.close()


def get_report_by_id(report_id):
    """Retrieve a single report by its ID."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM inspection_reports WHERE report_id = ?",
        (report_id,),
    )

    report = cursor.fetchone()

    conn.close()

    return report
