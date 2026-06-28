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

st.subheader("Saved Inspection Reports")

saved_reports = get_all_reports()

if saved_reports:
    st.dataframe(saved_reports)
else:
    st.info("No saved reports yet.")