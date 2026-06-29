import time

import pandas as pd
import streamlit as st

from database import create_database, get_all_reports, save_report
from llm import generate_report
from normalizer import normalize_ai_output

st.set_page_config(
    page_title="FieldForm AI",
    page_icon="📝",
    layout="wide"
)

st.title("📝 FieldForm AI")

st.markdown("""
### Offline AI-Powered Field Inspection Assistant

Convert unstructured field inspection notes into validated structured reports using a **local CPU-based Large Language Model (LLM)**.
""")

st.success(
    "🟢 Offline Mode Active   |   🤖 Local Ollama AI   |   💾 SQLite Database   |   🖥 CPU-Only Inference"
)

st.divider()

st.subheader("Inspection Notes")
create_database()
inspection_notes = st.text_area(
    "Enter Inspection Notes",
    height=300,
    placeholder="""Example:

Site visit at Government High School.

Approximately 120 students present.

Roof leakage observed in Block A.

Drinking water facility unavailable.

Electrical wiring exposed in the science laboratory.

Immediate repair recommended.
"""
)

if st.button(
    "🚀 Generate Structured Report",
    use_container_width=True,
    type="primary"
):
    if inspection_notes.strip():
        try:
            with st.spinner("Generating and saving structured report..."):
                start_time = time.perf_counter()
                ai_output = generate_report(inspection_notes)
                elapsed_time = time.perf_counter() - start_time
                report = normalize_ai_output(ai_output)
                save_report(report)
            st.session_state["last_saved"] = True
            st.success("✅ Report generated and saved successfully!")

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("People", report.people_count)
            col2.metric("Issues", len(report.issues))
            col3.metric("Severity", report.severity.value)
            col4.metric("Confidence", f"{report.confidence_score:.2f}")
            col5.metric("Inference", f"{elapsed_time:.2f}s")
            st.subheader("📄 Normalized Inspection Report")

            st.json(report.model_dump(mode="json"))

        except Exception as error:
            st.error("Failed to generate report.")
            with st.expander("Technical Details"):
                st.exception(error)
    else:
        st.warning("Please enter inspection notes.")

st.subheader("📊 Dashboard Statistics")

saved_reports = get_all_reports()

if saved_reports:
    total_reports = len(saved_reports)
    high_severity_count = sum(1 for report in saved_reports if report[11] == "High")
    pending_count = sum(1 for report in saved_reports if report[13] == "Pending")
    avg_confidence = round(
        sum(report[14] for report in saved_reports) / total_reports,
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reports", total_reports)
    col2.metric("High Severity", high_severity_count)
    col3.metric("Pending", pending_count)
    col4.metric("Avg Confidence", round(avg_confidence, 2))

if saved_reports:
    columns = [
        "Report ID",
        "Inspection Date",
        "State",
        "District",
        "Location",
        "Institution",
        "Institution Type",
        "Inspector",
        "Summary",
        "People",
        "Issues",
        "Severity",
        "Recommended Actions",
        "Status",
        "Confidence",
    ]

    df = pd.DataFrame(saved_reports, columns=columns)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No saved reports yet.")