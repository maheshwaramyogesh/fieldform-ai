import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from database import (create_database, delete_report, get_all_reports,
                      save_report, update_status)
from llm import generate_report
from normalizer import normalize_ai_output
from pdf_export import generate_pdf
from speech import transcribe_audio

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="FieldForm AI — Inspection Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "FieldForm AI — Offline AI-Powered Field Inspection & Survey Platform",
    },
)

PRIMARY = "#6C63FF"
PRIMARY_DARK = "#4B3FE4"
ACCENT = "#00D9C0"
WARN = "#FFB347"
DANGER = "#FF4D6D"
OK = "#2ECC71"
CARD_BG = "rgba(255,255,255,0.04)"

SEVERITY_COLORS = {"High": DANGER, "Medium": WARN, "Low": OK}
STATUS_COLORS = {"Pending": WARN, "In Progress": PRIMARY, "Resolved": OK}

# ============================================================================
# SESSION STATE
# ============================================================================
if "nav" not in st.session_state:
    st.session_state.nav = "Record Inspection"
if "open_report" not in st.session_state:
    st.session_state.open_report = None
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "Text"

# ============================================================================
# GLOBAL CSS
# ============================================================================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    .hero {{
        background: linear-gradient(120deg, {PRIMARY_DARK} 0%, {PRIMARY} 45%, {ACCENT} 100%);
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
        border-radius: 22px;
        padding: 2.2rem 2.2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 10px 40px rgba(108,99,255,0.35);
        position: relative;
        overflow: hidden;
    }}
    .hero::after {{
        content: ""; position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 60%);
        animation: pulse 6s ease-in-out infinite;
    }}
    @keyframes gradientShift {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}
    @keyframes pulse {{ 0%,100%{{transform:scale(1);opacity:.6}} 50%{{transform:scale(1.15);opacity:.3}} }}
    .hero h1 {{ font-family:'Sora',sans-serif; font-weight:800; font-size:2.5rem; color:#fff; margin:0; letter-spacing:-.5px; position:relative; z-index:1; }}
    .hero p {{ color:rgba(255,255,255,.92); font-size:1.02rem; margin-top:.45rem; max-width:680px; position:relative; z-index:1; }}
    .badge-row {{ display:flex; gap:.55rem; margin-top:1rem; flex-wrap:wrap; position:relative; z-index:1; }}
    .pill {{ background:rgba(255,255,255,.18); backdrop-filter:blur(6px); border:1px solid rgba(255,255,255,.25);
             color:#fff; padding:.32rem .85rem; border-radius:999px; font-size:.8rem; font-weight:600; }}
    .live-dot {{ display:inline-block; width:8px; height:8px; border-radius:50%; background:#FF4D6D;
                 margin-right:6px; animation:blink 1.4s infinite; }}
    @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:.2}} }}

    .metric-card {{
        background:{CARD_BG}; border:1px solid rgba(255,255,255,.08); border-radius:16px;
        padding:1.05rem 1.15rem; transition:transform .25s ease, box-shadow .25s ease;
    }}
    .metric-card:hover {{ transform:translateY(-4px); box-shadow:0 8px 28px rgba(108,99,255,.25); border-color:{PRIMARY}; }}
    .metric-label {{ font-size:.75rem; color:#9aa0b4; font-weight:700; text-transform:uppercase; letter-spacing:.06em; margin-bottom:.3rem; }}
    .metric-value {{ font-family:'Sora',sans-serif; font-size:1.85rem; font-weight:700; color:#f0f1f8; }}
    .metric-delta {{ font-size:.78rem; font-weight:600; }}

    .sev-badge, .status-badge {{ display:inline-block; padding:.22rem .75rem; border-radius:999px; font-weight:700; font-size:.76rem; color:#fff; }}

    .issue-chip {{ background:rgba(255,77,109,.12); border-left:3px solid {DANGER}; padding:.5rem .8rem; border-radius:8px; margin-bottom:.4rem; font-size:.9rem; }}
    .action-chip {{ background:rgba(46,204,113,.12); border-left:3px solid {OK}; padding:.5rem .8rem; border-radius:8px; margin-bottom:.4rem; font-size:.9rem; }}

    .section-title {{ font-family:'Sora',sans-serif; font-weight:700; font-size:1.28rem; margin:.3rem 0 .85rem 0; color:#f0f1f8; }}
    .subtle {{ color:#9aa0b4; font-size:.85rem; }}

    .stButton > button {{
        background:linear-gradient(90deg,{PRIMARY_DARK},{PRIMARY}); color:#fff; border:none; border-radius:12px;
        padding:.65rem 1.3rem; font-weight:700; font-size:.96rem; transition:all .2s ease;
        box-shadow:0 4px 18px rgba(108,99,255,.4);
    }}
    .stButton > button:hover {{ transform:translateY(-2px) scale(1.01); box-shadow:0 8px 26px rgba(108,99,255,.55); }}

    .report-card {{ background:{CARD_BG}; border:1px solid rgba(255,255,255,.08); border-radius:18px; padding:1.6rem; margin-top:1rem; animation:fadeIn .5s ease; }}
    @keyframes fadeIn {{ from{{opacity:0; transform:translateY(10px)}} to{{opacity:1; transform:translateY(0)}} }}

    .nav-card {{ background:{CARD_BG}; border-radius:14px; padding:.4rem; }}

    .ring-wrap {{ display:flex; align-items:center; justify-content:center; gap:1.4rem; flex-wrap:wrap; }}

    #MainMenu {{visibility:hidden;}} footer {{visibility:hidden;}} header {{visibility:hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)

create_database()

# ============================================================================
# SIDEBAR — NAVIGATION + LIVE FILTERS
# ============================================================================
with st.sidebar:
    st.markdown("## 🛰️ FieldForm AI")
    st.caption("Offline AI inspection & survey platform")
    st.divider()

    st.session_state.nav = st.radio(
        "Navigate",
        ["Record Inspection", "Live Dashboard", "Analytics", "Report Explorer"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**System Status**")
    st.markdown("🟢 Offline Mode")
    st.markdown("🤖 Local Ollama LLM")
    st.markdown("💾 SQLite Storage")
    st.markdown("🖥️ CPU-Only Inference")
    st.divider()
    st.caption(f"Session: {datetime.now().strftime('%d %b %Y, %H:%M')}")

# ============================================================================
# HERO
# ============================================================================
all_reports_count = len(get_all_reports())
st.markdown(
    f"""
    <div class="hero">
        <h1>🛰️ FieldForm AI</h1>
        <p>An offline, AI-driven inspection and survey recording platform — capture field
        notes by text or voice, and get validated, structured, decision-ready reports in seconds.</p>
        <div class="badge-row">
            <span class="pill"><span class="live-dot"></span>Live Recording Ready</span>
            <span class="pill">🤖 Local Ollama AI</span>
            <span class="pill">💾 {all_reports_count} Reports Logged</span>
            <span class="pill">🖥️ CPU-Only Inference</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# PAGE: RECORD INSPECTION
# ============================================================================
if st.session_state.nav == "Record Inspection":
    st.markdown(
        '<div class="section-title">🎙️ Capture Inspection Notes</div>',
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Input mode",
        ["✍️ Type Notes", "🎙️ Record Voice Note"],
        horizontal=True,
        label_visibility="collapsed",
    )

    inspection_notes = ""

    if mode == "✍️ Type Notes":
        inspection_notes = st.text_area(
            "Enter Inspection Notes",
            height=240,
            placeholder="""Example:

Site visit at Government High School.
Approximately 120 students present.
Roof leakage observed in Block A.
Drinking water facility unavailable.
Electrical wiring exposed in the science laboratory.
Immediate repair recommended.""",
            label_visibility="collapsed",
        )
    else:
        st.info(
            """
🎙️ **Voice Recording Mode**

Record your inspection using your microphone.

**Current functionality**
- ✅ Audio recording is supported.
- ✅ Audio can be reviewed before submission.
- ⚡ Automatic speech-to-text transcription is planned for the next version.

For now, paste or type the transcript below to continue the AI pipeline.
""",
            icon="🎤",
        )
        audio = st.audio_input("🎙️ Record your inspection note")

        if audio is not None:
            st.audio(audio)

            with st.spinner("🎤 Transcribing audio..."):
                inspection_notes = transcribe_audio(audio)

            st.success("✅ Voice note transcribed successfully.")

        inspection_notes = st.text_area(
            "Inspection Transcript",
            value=inspection_notes,
            height=180,
        )

    c_btn, c_clear = st.columns([4, 1])
    generate_clicked = c_btn.button(
        "🚀 Generate Structured Report", use_container_width=True, type="primary"
    )
    clear_clicked = c_clear.button("🧹 Clear", use_container_width=True)

    if clear_clicked:
        st.rerun()

    if generate_clicked:
        if inspection_notes.strip():
            try:
                bar = st.progress(0, text="Warming up local model...")
                start_time = time.perf_counter()

                bar.progress(20, text="🧠 Reading inspection notes...")
                time.sleep(0.15)
                bar.progress(40, text="🤖 Running local LLM inference...")
                ai_output = generate_report(inspection_notes)

                bar.progress(75, text="🧩 Normalizing structured fields...")
                report = normalize_ai_output(ai_output)

                bar.progress(92, text="💾 Saving to database...")
                save_report(report)

                elapsed_time = time.perf_counter() - start_time
                bar.progress(100, text="✅ Done!")
                time.sleep(0.25)
                bar.empty()

                st.toast("Report generated and saved!", icon="✅")

                cols = st.columns(5)
                metric_data = [
                    ("👥 People", report.people_count),
                    ("⚠️ Issues", len(report.issues)),
                    ("🚦 Severity", report.severity.value),
                    ("🎯 Confidence", f"{report.confidence_score:.0%}"),
                    ("⏱️ Inference", f"{elapsed_time:.2f}s"),
                ]
                for col, (label, value) in zip(cols, metric_data):
                    col.markdown(
                        f"""<div class="metric-card"><div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div></div>""",
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                sev_color = SEVERITY_COLORS.get(report.severity.value, PRIMARY)
                st.markdown('<div class="report-card">', unsafe_allow_html=True)

                top1, top2 = st.columns([3, 1])
                with top1:
                    st.markdown(f"#### 🏫 {report.institution_name}")
                    st.caption(
                        f"{report.institution_type} · {report.location}, {report.district}, {report.state}"
                    )
                with top2:
                    st.markdown(
                        f'<span class="sev-badge" style="background:{sev_color};">{report.severity.value} Severity</span>',
                        unsafe_allow_html=True,
                    )

                st.markdown(f"**📋 Summary:** {report.summary}")

                meta1, meta2, meta3 = st.columns(3)
                meta1.markdown(f"**Inspector:** {report.inspector_name}")
                meta2.markdown(f"**Date:** {report.inspection_date}")
                meta3.markdown(f"**Report ID:** `{report.report_id}`")

                st.markdown("---")
                issue_col, action_col = st.columns(2)
                with issue_col:
                    st.markdown("**🔴 Issues Identified**")
                    for issue in report.issues:
                        st.markdown(
                            f'<div class="issue-chip">⚠️ {issue}</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown("</div>", unsafe_allow_html=True)

                with st.expander("🔎 View Raw JSON"):
                    st.json(report.model_dump(mode="json"))

                    pdf_buffer = generate_pdf(report)

                st.download_button(
                    label="📄 Download Inspection Report (PDF)",
                    data=pdf_buffer,
                    file_name=f"{report.report_id}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

            except Exception as error:
                st.error("Failed to generate report.")
                with st.expander("Technical Details"):
                    st.exception(error)
        else:
            st.warning("Please enter or transcribe inspection notes first.")

# ============================================================================
# PAGE: LIVE DASHBOARD
# ============================================================================
elif st.session_state.nav == "Live Dashboard":
    saved_reports = get_all_reports()

    if not saved_reports:
        st.info(
            "No saved reports yet. Go to **Record Inspection** to create your first one."
        )
    else:
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
        st.markdown(
            '<div class="section-title">🔎 Search Reports</div>', unsafe_allow_html=True
        )

        search_text = st.text_input(
            "Search saved reports",
            placeholder="Search by report ID, institution, location, district, or state",
        )
        st.subheader("📊 Inspection Analytics")

        severity_counts = (
            df["Severity"]
            .value_counts()
            .rename_axis("Severity")
            .reset_index(name="Count")
        )

        fig = px.bar(
            severity_counts,
            x="Severity",
            y="Count",
            color="Severity",
            title="Reports by Severity",
        )

        st.plotly_chart(fig, use_container_width=True)

        total_reports = len(df)
        high_severity_count = int((df["Severity"] == "High").sum())
        pending_count = int((df["Status"] == "Pending").sum())
        resolved_count = int((df["Status"] == "Resolved").sum())
        avg_confidence = df["Confidence"].mean()

        st.markdown(
            '<div class="section-title">📊 Live Overview</div>', unsafe_allow_html=True
        )
        c1, c2, c3, c4, c5 = st.columns(5)
        stats = [
            ("📁 Total Reports", total_reports, "All inspections stored"),
            ("🔴 High Severity", high_severity_count, "Immediate attention"),
            ("⏳ Pending", pending_count, "Awaiting action"),
            ("✅ Resolved", resolved_count, "Successfully closed"),
            ("🎯 Avg Confidence", f"{avg_confidence:.0%}", "AI extraction quality"),
        ]
        for col, (label, value, subtitle) in zip([c1, c2, c3, c4, c5], stats):
            col.markdown(
                f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div style="color:#94A3B8;font-size:12px;margin-top:6px;">
            {subtitle}
        </div>
    </div>
    """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        status_counts = (
            df["Status"].value_counts().rename_axis("Status").reset_index(name="Count")
        )

        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Inspection Status Distribution",
        )

        st.markdown("---")

        timeline = df.groupby("Inspection Date").size().reset_index(name="Reports")

        timeline["Inspection Date"] = pd.to_datetime(timeline["Inspection Date"])

        timeline = timeline.sort_values("Inspection Date")

        fig_timeline = px.line(
            timeline,
            x="Inspection Date",
            y="Reports",
            markers=True,
            title="Inspection Reports Over Time",
        )

        col_left, col_right = st.columns(2)

        with col_left:
            st.plotly_chart(fig_timeline, use_container_width=True)

        with col_right:
            st.plotly_chart(fig_status, use_container_width=True)

            st.markdown("---")

        location_counts = (
            df.groupby("Location")
            .size()
            .reset_index(name="Reports")
            .sort_values("Reports", ascending=False)
            .head(5)
        )

        fig_locations = px.bar(
            location_counts,
            x="Reports",
            y="Location",
            orientation="h",
            title="Top Inspection Locations",
            text="Reports",
        )

        fig_locations.update_layout(
            yaxis=dict(autorange="reversed"),
            height=420,
        )

        st.plotly_chart(fig_locations, use_container_width=True)

        st.markdown("---")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">🔍 Filter Reports</div>', unsafe_allow_html=True
        )

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            sev_filter = st.multiselect(
                "Severity", ["High", "Medium", "Low"], default=[]
            )
        with f2:
            status_filter = st.multiselect(
                "Status", ["Pending", "In Progress", "Resolved"], default=[]
            )
        with f3:
            search_term = st.text_input("Search institution / location", "")
        with f4:
            sort_by = st.selectbox(
                "Sort by", ["Inspection Date", "Confidence", "People"], index=0
            )

        filtered = df.copy()
        if sev_filter:
            filtered = filtered[filtered["Severity"].isin(sev_filter)]
        if status_filter:
            filtered = filtered[filtered["Status"].isin(status_filter)]
        if search_term:
            mask = filtered["Institution"].str.contains(
                search_term, case=False, na=False
            ) | filtered["Location"].str.contains(search_term, case=False, na=False)
            filtered = filtered[mask]
        filtered = filtered.sort_values(sort_by, ascending=False)

        st.markdown(
            f'<div class="subtle">Showing {len(filtered)} of {total_reports} reports</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">✏️ Editable Report Table</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Change the Status column directly — updates save to the database instantly."
    )

    edited = st.data_editor(
        filtered,
        use_container_width=True,
        height=420,
        hide_index=True,
        disabled=[c for c in columns if c != "Status"],
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status", options=["Pending", "In Progress", "Resolved"], required=True
            ),
            "Confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0.0, max_value=1.0, format="%.0f%%"
            ),
        },
        key="report_editor",
    )

    if not edited.equals(filtered):
        changed = edited[edited["Status"] != filtered["Status"]]
        for _, row in changed.iterrows():
            update_status(row["Report ID"], row["Status"])
        if len(changed):
            st.toast(f"Updated status for {len(changed)} report(s).", icon="💾")
            st.rerun()

    csv = filtered.to_csv(index=False).encode("utf-8")
    dl1, dl2 = st.columns(2)
    dl1.download_button(
        "⬇️ Export CSV",
        csv,
        "fieldform_reports.csv",
        "text/csv",
        use_container_width=True,
    )
    dl2.download_button(
        "⬇️ Export JSON",
        filtered.to_json(orient="records", indent=2),
        "fieldform_reports.json",
        "application/json",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">🗑️ Remove a Report</div>', unsafe_allow_html=True
    )
    del_col1, del_col2 = st.columns([3, 1])
    report_to_delete = del_col1.selectbox(
        "Report ID", options=filtered["Report ID"].tolist()
    )
    if del_col2.button("Delete", use_container_width=True):
        delete_report(report_to_delete)
        st.toast(f"Deleted {report_to_delete}", icon="🗑️")
        st.rerun()

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================
elif st.session_state.nav == "Analytics":
    saved_reports = get_all_reports()

    if not saved_reports:
        st.info("No data to analyze yet. Generate a few reports first.")
    else:
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
        df["Inspection Date"] = pd.to_datetime(df["Inspection Date"], errors="coerce")

        # --- Confidence gauge ---
        st.markdown(
            '<div class="section-title">🎯 Overall Confidence Health</div>',
            unsafe_allow_html=True,
        )
        avg_conf = df["Confidence"].mean()
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_conf * 100,
                number={"suffix": "%", "font": {"color": "#f0f1f8"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#9aa0b4"},
                    "bar": {"color": ACCENT},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(255,77,109,0.25)"},
                        {"range": [50, 80], "color": "rgba(255,179,71,0.25)"},
                        {"range": [80, 100], "color": "rgba(46,204,113,0.25)"},
                    ],
                },
            )
        )
        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f1f8"),
            margin=dict(t=20, b=10, l=20, r=20),
            height=260,
        )
        st.plotly_chart(gauge, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<div class="section-title">Severity Distribution</div>',
                unsafe_allow_html=True,
            )
            sev_counts = df["Severity"].value_counts()
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=sev_counts.index,
                        values=sev_counts.values,
                        hole=0.55,
                        marker=dict(
                            colors=[
                                SEVERITY_COLORS.get(s, "#888") for s in sev_counts.index
                            ]
                        ),
                        textinfo="label+percent",
                    )
                ]
            )
            fig.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f1f8"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(
                '<div class="section-title">Status Breakdown</div>',
                unsafe_allow_html=True,
            )
            status_counts = df["Status"].value_counts()
            fig2 = go.Figure(
                data=[
                    go.Bar(
                        x=status_counts.index,
                        y=status_counts.values,
                        marker=dict(
                            color=[
                                STATUS_COLORS.get(s, ACCENT)
                                for s in status_counts.index
                            ]
                        ),
                    )
                ]
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f1f8"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            '<div class="section-title">Reports Over Time</div>', unsafe_allow_html=True
        )
        timeline = (
            df.dropna(subset=["Inspection Date"])
            .groupby(df["Inspection Date"].dt.date)
            .size()
            .reset_index(name="count")
        )
        fig3 = go.Figure(
            data=[
                go.Scatter(
                    x=timeline["Inspection Date"],
                    y=timeline["count"],
                    mode="lines+markers",
                    line=dict(color=PRIMARY, width=3),
                    marker=dict(size=8, color=ACCENT),
                    fill="tozeroy",
                    fillcolor="rgba(108,99,255,0.12)",
                )
            ]
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f1f8"),
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        )
        st.plotly_chart(fig3, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                '<div class="section-title">Top Institutions by Reports</div>',
                unsafe_allow_html=True,
            )
            top_inst = df["Institution"].value_counts().head(8)
            fig4 = go.Figure(
                data=[
                    go.Bar(
                        x=top_inst.values,
                        y=top_inst.index,
                        orientation="h",
                        marker=dict(color=ACCENT),
                    )
                ]
            )
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f1f8"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig4, use_container_width=True)

        with col4:
            st.markdown(
                '<div class="section-title">People Present vs Confidence</div>',
                unsafe_allow_html=True,
            )
            fig5 = go.Figure(
                data=[
                    go.Scatter(
                        x=df["People"],
                        y=df["Confidence"],
                        mode="markers",
                        marker=dict(
                            size=12,
                            color=[
                                SEVERITY_COLORS.get(s, "#888") for s in df["Severity"]
                            ],
                            line=dict(width=1, color="white"),
                        ),
                        text=df["Institution"],
                    )
                ]
            )
            fig5.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f1f8"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
                xaxis=dict(title="People Present", gridcolor="rgba(255,255,255,0.07)"),
                yaxis=dict(
                    title="Confidence", range=[0, 1], gridcolor="rgba(255,255,255,0.07)"
                ),
            )
            st.plotly_chart(fig5, use_container_width=True)

# ============================================================================
# PAGE: REPORT EXPLORER (card-based detail browser)
# ============================================================================
elif st.session_state.nav == "Report Explorer":
    saved_reports = get_all_reports()

    if not saved_reports:
        st.info(
            "No saved reports yet. Go to **Record Inspection** to create your first one."
        )
    else:
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
        saved_reports = get_all_reports()
df = pd.DataFrame(saved_reports, columns=columns)

st.markdown(
    '<div class="section-title">🗂️ Report Explorer</div>', unsafe_allow_html=True
)

search_text = st.text_input(
    "🔎 Search reports",
    placeholder="Search by report ID, institution, location, district, or state",
)

view = df.copy()

if search_text:
    search_lower = search_text.lower()

    mask = (
        view["Report ID"].astype(str).str.lower().str.contains(search_lower, na=False)
        | view["Institution"]
        .astype(str)
        .str.lower()
        .str.contains(search_lower, na=False)
        | view["Location"].astype(str).str.lower().str.contains(search_lower, na=False)
        | view["District"].astype(str).str.lower().str.contains(search_lower, na=False)
        | view["State"].astype(str).str.lower().str.contains(search_lower, na=False)
    )

    view = view[mask]

st.caption(f"{len(view)} matching report(s) found")

for _, row in view.iterrows():

    report_id = row["Report ID"]

    with st.expander(
        f"📄 {report_id} - {row['Institution']} ({row['Location']}, {row['District']})"
    ):
        st.markdown(f"**Inspection Date:** {row['Inspection Date']}")
        st.markdown(f"**State:** {row['State']}")
        st.markdown(f"**District:** {row['District']}")
        st.markdown(f"**Location:** {row['Location']}")
        st.markdown(f"**Institution Type:** {row['Institution Type']}")
        st.markdown(f"**Inspector:** {row['Inspector']}")
        st.markdown(f"**Summary:** {row['Summary']}")
        st.markdown(f"**People Present:** {row['People']}")
        st.markdown(f"**Issues Identified:** {row['Issues']}")
        st.markdown(f"**Severity:** {row['Severity']}")
        st.markdown(f"**Recommended Actions:** {row['Recommended Actions']}")
        st.markdown(f"**Status:** {row['Status']}")
        st.markdown(f"**Confidence Score:** {row['Confidence']:.0%}")
