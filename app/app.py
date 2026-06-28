import streamlit as st
from llm import generate_report

st.set_page_config(
    page_title="FieldForm AI",
    page_icon="📝",
    layout="wide"
)

st.title("📝 FieldForm AI")

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
        with st.spinner("Generating structured report..."):
            report = generate_report(inspection_notes)

        st.success("Report generated successfully!")

        st.json(report)

    else:
        st.warning("Please enter inspection notes.")