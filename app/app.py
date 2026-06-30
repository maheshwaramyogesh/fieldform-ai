import json
import streamlit as st

from llm import generate_report
from normalizer import normalize_ai_output
from database import create_database, save_report, get_all_reports

st.set_page_config(
    page_title="FieldForm AI",
    page_icon="📝",
    layout="wide"
)

st.title("📝 FieldForm AI")

create_database()

st.markdown(
    """
    ### Offline AI-Powered Field Survey & Inspection Assistant

    This application converts unstructured field inspection notes into structured JSON records using a local CPU-based AI model.
    """
)

inspection_notes = st.text_area(
    "Enter Inspection Notes",
    height=250,
    placeholder="Example:\nVisited Government School.\nRoof leaking.\nApproximately 150 students.\nNeeds urgent repair."
)

if st.button("Generate Structured Report"):
    if inspection_notes.strip():
        try:
            with st.spinner("Generating and saving structured report..."):
                ai_output = generate_report(inspection_notes)
                report = normalize_ai_output(ai_output)
                save_report(report)
                st.session_state["last_saved"] = True
            st.success("Report generated and saved successfully!")
            st.json(report.model_dump(mode="json"))

        except Exception as error:
            st.error(f"Error: {error}")
    else:
        st.warning("Please enter inspection notes.")

st.subheader("Dashboard Statistics")

saved_reports = get_all_reports()

if saved_reports:
    total_reports = len(saved_reports)
    high_severity_count = sum(1 for report in saved_reports if report[11] == "High")
    pending_count = sum(1 for report in saved_reports if report[13] == "Pending")
    avg_confidence = sum(report[14] for report in saved_reports) / total_reports

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reports", total_reports)
    col2.metric("High Severity", high_severity_count)
    col3.metric("Pending", pending_count)
    col4.metric("Avg Confidence", round(avg_confidence, 2))

    st.subheader("Saved Inspection Reports")

if saved_reports:
    st.dataframe(saved_reports)

    reports_json = json.dumps(saved_reports, indent=2)

    st.download_button(
        label="Download Reports as JSON",
        data=reports_json,
        file_name="inspection_reports.json",
        mime="application/json",
    )

else:
    st.info("No saved reports yet.")