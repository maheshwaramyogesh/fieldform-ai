from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_pdf(report):
    """
    Generate a PDF inspection report.

    Returns:
        BytesIO object containing the PDF.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>FieldForm AI Inspection Report</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Report ID:</b> {report.report_id}", styles["Normal"]))
    story.append(Paragraph(f"<b>Date:</b> {report.inspection_date}", styles["Normal"]))
    story.append(
        Paragraph(f"<b>Inspector:</b> {report.inspector_name}", styles["Normal"])
    )
    story.append(
        Paragraph(f"<b>Institution:</b> {report.institution_name}", styles["Normal"])
    )
    story.append(Paragraph(f"<b>Location:</b> {report.location}", styles["Normal"]))
    story.append(Paragraph(f"<b>State:</b> {report.state}", styles["Normal"]))
    story.append(Paragraph(f"<b>District:</b> {report.district}", styles["Normal"]))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    story.append(Paragraph(report.summary, styles["Normal"]))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Issues Identified</b>", styles["Heading2"]))

    if report.issues:
        for issue in report.issues:
            story.append(Paragraph(f"• {issue}", styles["Normal"]))
    else:
        story.append(Paragraph("No issues reported.", styles["Normal"]))

    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Recommended Actions</b>", styles["Heading2"]))

    if report.recommended_actions:
        for action in report.recommended_actions:
            story.append(Paragraph(f"• {action}", styles["Normal"]))
    else:
        story.append(Paragraph("No recommended actions.", styles["Normal"]))

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Severity:</b> {report.severity.value}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Status:</b> {report.status.value}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {report.confidence_score:.0%}",
            styles["Normal"],
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer
