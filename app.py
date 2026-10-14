"""
app.py
======
Main Streamlit Web Application:
"Personalized Report Generation using Templates and Python"

Master of Computer Applications (MCA) Coursework
Theme: Warm Cream Background with High-Contrast Espresso Typography
"""

import streamlit as st
import pandas as pd

# Core Project Modules
from src.data_processor import (
    validate_student_inputs,
    process_student_data,
    assign_performance_category
)
from src.visualizer import generate_performance_chart
from src.template_engine import render_html_report_preview, DEFAULT_REPORT_CONFIG
from src.pdf_generator import generate_pdf_report
from sample_data import SAMPLE_STUDENTS, DEFAULT_SUBJECT_NAMES, DEPARTMENTS, SEMESTERS

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Personalized Report Generation | MCA Academic System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern warm cream academic dashboard styling
st.markdown("""
<style>
    /* Warm Cream Canvas for Entire Application */
    .stApp {
        background-color: #FAF7EE !important;
        color: #2A201A !important;
    }
    
    .main {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #FAF7EE !important;
    }
    
    /* Header Card with Rich Warm Espresso Gradient */
    .main-header {
        background: linear-gradient(135deg, #3A2A1E 0%, #20150F 100%);
        color: #FFFDF9;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(50, 30, 15, 0.15);
        border: 1px solid #523C2D;
    }
    .main-header h1 {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        color: #FFF8EE !important;
        letter-spacing: -0.3px;
    }
    .main-header p {
        font-size: 14px;
        color: #DBCAB7 !important;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* High Visibility Typography on Cream Canvas */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p {
        color: #2A201A !important;
    }
    .main-header h1, .main-header p {
        color: #FFF8EE !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F3EDE2 !important;
        border-right: 1px solid #E2D7C7 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #2A201A !important;
    }
    .sidebar-box {
        background-color: #FFFDF8;
        border: 1px solid #E2D7C7;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 16px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFDF8 !important;
        border: 1px solid #E5DACB !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        box-shadow: 0 2px 8px rgba(70, 50, 30, 0.05) !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #6B5848 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #2A201A !important;
        font-weight: 800 !important;
        font-size: 22px !important;
    }

    /* Form Input Fields Visibility */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-color: #D6C8B5 !important;
        border-radius: 8px !important;
    }
    input {
        color: #2A201A !important;
    }

    /* =========================================================================
       BUTTON STYLING: Rich Warm Mahogany Background with Crisp Pure White Text
       Guarantees high contrast and 100% text readability
       ========================================================================= */
    .stButton > button,
    .stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background: linear-gradient(135deg, #78350F 0%, #5C270A 100%) !important;
        border: 1px solid #451A03 !important;
        border-radius: 8px !important;
        padding: 11px 22px !important;
        box-shadow: 0 2px 6px rgba(69, 26, 3, 0.22) !important;
        transition: all 0.2s ease !important;
    }

    /* Force all inner text, p, div, span inside buttons to be Crisp White */
    .stButton > button *,
    .stButton > button p,
    .stButton > button div,
    .stButton > button span,
    .stDownloadButton > button *,
    .stDownloadButton > button p,
    .stDownloadButton > button div,
    .stDownloadButton > button span,
    div[data-testid="stFormSubmitButton"] > button *,
    div[data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stFormSubmitButton"] > button div,
    div[data-testid="stFormSubmitButton"] > button span {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.3px !important;
    }

    /* Button Hover State */
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #92400E 0%, #78350F 100%) !important;
        border-color: #5C270A !important;
        box-shadow: 0 4px 10px rgba(69, 26, 3, 0.28) !important;
    }

    .stButton > button:hover *,
    .stDownloadButton > button:hover *,
    div[data-testid="stFormSubmitButton"] > button:hover * {
        color: #FFFDF9 !important;
    }

    /* Tab Headers */
    button[data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #78350F !important;
        border-bottom-color: #78350F !important;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Session State Initialization
# -----------------------------------------------------------------------------
if "report_data" not in st.session_state:
    st.session_state.report_data = None
if "chart_bytes" not in st.session_state:
    st.session_state.chart_bytes = None
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

# Initialize form field state defaults with Induja (MCA - 25MX101)
default_sample_key = "Induja (High Achiever - Excellent)"
init_data = SAMPLE_STUDENTS[default_sample_key]

if "name_val" not in st.session_state:
    st.session_state.name_val = init_data["name"]
if "roll_val" not in st.session_state:
    st.session_state.roll_val = init_data["roll_no"]
if "dept_val" not in st.session_state:
    st.session_state.dept_val = init_data["department"]
if "sem_val" not in st.session_state:
    st.session_state.sem_val = init_data["semester"]
if "att_val" not in st.session_state:
    st.session_state.att_val = float(init_data["attendance"])
for sub in DEFAULT_SUBJECT_NAMES:
    key = f"mark_{sub}"
    if key not in st.session_state:
        st.session_state[key] = float(init_data["subjects"].get(sub, 75))


def load_preset(student_key: str):
    """Callback to populate form fields with sample data."""
    selected = SAMPLE_STUDENTS[student_key]
    st.session_state.name_val = selected["name"]
    st.session_state.roll_val = selected["roll_no"]
    st.session_state.dept_val = selected["department"]
    st.session_state.sem_val = selected["semester"]
    st.session_state.att_val = float(selected["attendance"])
    for sub in DEFAULT_SUBJECT_NAMES:
        key = f"mark_{sub}"
        st.session_state[key] = float(selected["subjects"].get(sub, 75))
    # Clear previous report to trigger fresh generation
    st.session_state.report_data = None
    st.session_state.chart_bytes = None
    st.session_state.pdf_bytes = None


# -----------------------------------------------------------------------------
# 3. Sidebar: Quick Presets & Technical Architecture
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/graduation-cap.svg",
        width=44
    )
    st.markdown("### Classroom Demo Presets")
    st.caption("Select a pre-configured student profile to populate the form instantly for presentation:")

    chosen_preset = st.selectbox(
        "Select Profile:",
        options=list(SAMPLE_STUDENTS.keys()),
        index=0
    )

    if st.button("Load Selected Profile", use_container_width=True):
        load_preset(chosen_preset)
        st.toast(f"Loaded {chosen_preset.split('(')[0].strip()}'s profile successfully.", icon="✔")

    st.markdown("---")
    st.markdown("### Technology Architecture")
    st.markdown("""
    - **Language:** Python 3.11
    - **Web Framework:** Streamlit
    - **Data Pipeline:** Pandas
    - **Visual Analytics:** Matplotlib (`Agg`)
    - **Document Engine:** ReportLab Platypus
    - **Design Pattern:** Decoupled Template Engine
    """)

    st.markdown("---")
    st.markdown("### Grading Standards & Thresholds")
    st.markdown("""
    * **Excellent (Honors):** $\ge 85\%$
    * **Good (Consistent):** $70\% - 84.9\%$
    * **Average (Pass):** $50\% - 69.9\%$
    * **Needs Improvement:** $< 50\%$
    * **Attendance Eligibility:** $\ge 75\%$
    """)


# -----------------------------------------------------------------------------
# 4. Main Page Header
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>Personalized Report Generation using Templates and Python</h1>
    <p>Department of Computer Applications (MCA) &bull; Automated Academic Appraisal & Vector PDF Generation System</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Two-Tab Layout: [1] Student Input Form | [2] Live Report & PDF
# -----------------------------------------------------------------------------
tab_input, tab_preview = st.tabs(["1. Student Information & Marks Entry", "2. Academic Report & PDF Export"])

with tab_input:
    st.markdown("#### Student Coursework Information")
    st.info("**Quick Guidance:** Load sample student profiles from the sidebar presets or enter custom coursework marks below.")

    with st.form("student_input_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Student Identification")
            name_input = st.text_input(
                "Full Name:",
                value=st.session_state.name_val,
                placeholder="e.g. Induja",
                help="Enter student's official registered full name."
            )
            roll_input = st.text_input(
                "Roll Number / Registration ID:",
                value=st.session_state.roll_val,
                placeholder="e.g. 25MX101",
                help="Unique student identification number (25MX--- format)."
            )
            dept_input = st.selectbox(
                "Academic Department (Recommended: MCA):",
                options=DEPARTMENTS,
                index=DEPARTMENTS.index(st.session_state.dept_val) if st.session_state.dept_val in DEPARTMENTS else 0
            )

        with col2:
            st.markdown("##### Enrollment & Attendance")
            sem_input = st.selectbox(
                "Current Semester:",
                options=SEMESTERS,
                index=SEMESTERS.index(st.session_state.sem_val) if st.session_state.sem_val in SEMESTERS else 2
            )
            att_input = st.number_input(
                "Attendance Percentage (%):",
                min_value=0.0,
                max_value=100.0,
                value=float(st.session_state.att_val),
                step=0.5,
                help="Minimum mandatory university threshold is 75%."
            )

        st.markdown("---")
        st.markdown("##### Coursework Marks (Scale 0–100)")

        sub_cols = st.columns(5)
        entered_subjects = {}

        for idx, sub_name in enumerate(DEFAULT_SUBJECT_NAMES):
            with sub_cols[idx]:
                key = f"mark_{sub_name}"
                val = st.number_input(
                    label=sub_name,
                    min_value=0.0,
                    max_value=100.0,
                    value=float(st.session_state.get(key, 75.0)),
                    step=1.0,
                    key=f"form_input_{idx}"
                )
                entered_subjects[sub_name] = val

        st.markdown("<br>", unsafe_allow_html=True)
        generate_clicked = st.form_submit_button("Generate Academic Report", use_container_width=True, type="primary")

    # Handle Form Submission & Validation
    if generate_clicked:
        # 1. Validation
        is_valid, validation_errors = validate_student_inputs(
            name=name_input,
            roll_no=roll_input,
            department=dept_input,
            semester=sem_input,
            attendance=att_input,
            subjects=entered_subjects
        )

        if not is_valid:
            st.error("**Validation Notice:** Please correct the following inputs before proceeding:")
            for err in validation_errors:
                st.write(f"- {err}")
        else:
            # 2. Data Processing & Statistical Aggregation
            payload = {
                "name": name_input,
                "roll_no": roll_input,
                "department": dept_input,
                "semester": sem_input,
                "attendance": att_input,
                "subjects": entered_subjects
            }
            with st.spinner("Processing marks, applying appraisal rules, and compiling graphics..."):
                processed_results = process_student_data(payload)

                # 3. Chart Generation (Matplotlib)
                fig, chart_png_bytes = generate_performance_chart(
                    subjects=entered_subjects,
                    student_name=processed_results["student_info"]["name"],
                    average_mark=processed_results["metrics"]["average_marks"]
                )

                # 4. PDF Generation (ReportLab)
                pdf_output_bytes = generate_pdf_report(
                    processed_data=processed_results,
                    chart_image_bytes=chart_png_bytes,
                    institution_config=DEFAULT_REPORT_CONFIG
                )

                # Save into session state for persistent preview and download
                st.session_state.report_data = processed_results
                st.session_state.chart_bytes = chart_png_bytes
                st.session_state.chart_fig = fig
                st.session_state.pdf_bytes = pdf_output_bytes

            st.success("**Report Successfully Generated.** You can now review the analysis in Tab 2.")


# -----------------------------------------------------------------------------
# 6. Tab 2: Report Preview, Chart, Feedback & PDF Download
# -----------------------------------------------------------------------------
with tab_preview:
    if st.session_state.report_data is None:
        # Proactively generate initial report using default values so page isn't empty
        default_payload = {
            "name": st.session_state.name_val,
            "roll_no": st.session_state.roll_val,
            "department": st.session_state.dept_val,
            "semester": st.session_state.sem_val,
            "attendance": st.session_state.att_val,
            "subjects": {
                sub: float(st.session_state.get(f"mark_{sub}", 75.0))
                for sub in DEFAULT_SUBJECT_NAMES
            }
        }
        res = process_student_data(default_payload)
        fig, chart_png = generate_performance_chart(
            subjects=default_payload["subjects"],
            student_name=res["student_info"]["name"],
            average_mark=res["metrics"]["average_marks"]
        )
        pdf_b = generate_pdf_report(
            processed_data=res,
            chart_image_bytes=chart_png,
            institution_config=DEFAULT_REPORT_CONFIG
        )
        st.session_state.report_data = res
        st.session_state.chart_bytes = chart_png
        st.session_state.chart_fig = fig
        st.session_state.pdf_bytes = pdf_b

    rep = st.session_state.report_data
    metrics = rep["metrics"]
    student = rep["student_info"]

    # Top Action Bar with Download Button
    col_title, col_btn = st.columns([2.5, 1])
    with col_title:
        st.markdown(f"### Performance Report: **{student['name']}** ({student['roll_no']})")
    with col_btn:
        safe_name = student["name"].replace(" ", "_")
        pdf_filename = f"Performance_Report_{safe_name}_{student['roll_no']}.pdf"
        st.download_button(
            label="Download Official PDF Report",
            data=st.session_state.pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

    # Key Statistics Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric(
            label="Total Marks",
            value=f"{metrics['total_marks']:.0f} / {metrics['max_marks']}",
            delta=f"{metrics['percentage']:.1f}% Aggregate"
        )
    with m2:
        st.metric(
            label="Average Score",
            value=f"{metrics['average_marks']:.1f} / 100"
        )
    with m3:
        st.metric(
            label="Category",
            value=metrics["category"],
            delta="Standing: " + ("Pass" if metrics["percentage"] >= 50 else "Warning")
        )
    with m4:
        st.metric(
            label="Attendance",
            value=f"{student['attendance']:.1f}%",
            delta=student["attendance_status"],
            delta_color="normal" if student["attendance"] >= 75 else "inverse"
        )
    with m5:
        st.metric(
            label="Highest Subject",
            value=f"{metrics['highest_subject'][1]:.0f}/100",
            delta=metrics["highest_subject"][0][:18] + "..." if len(metrics["highest_subject"][0]) > 18 else metrics["highest_subject"][0]
        )

    st.markdown("---")

    # Split View: Left Column = Matplotlib Chart, Right Column = Coursework Table & Insights
    c_chart, c_table = st.columns([1.2, 1])

    with c_chart:
        st.markdown("##### Comparative Performance Analytics")
        st.pyplot(st.session_state.chart_fig, use_container_width=True)

    with c_table:
        st.markdown("##### Coursework Performance Breakdown")
        df_display = rep["dataframe"][["Subject Name", "Marks Obtained", "Grade", "Status"]]
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("##### Academic Highlights")
        st.markdown(f"- **Top Scoring Subject:** `{metrics['highest_subject'][0]}` ({metrics['highest_subject'][1]:.0f}/100)")
        st.markdown(f"- **Lowest Scoring Subject:** `{metrics['lowest_subject'][0]}` ({metrics['lowest_subject'][1]:.0f}/100)")
        st.markdown(f"- **Evaluation Standing:** {metrics['category_desc']}")

    st.markdown("---")

    # Personalized Feedback Callout
    st.markdown("##### Personalized Appraisal & Faculty Recommendations")
    for fb_point in rep["feedback"]:
        if "Shortage Alert" in fb_point or "Remedial Priority" in fb_point or "Remedial Advisory" in fb_point:
            st.warning(fb_point)
        elif "Honors Commendation" in fb_point or "Academic Distinction" in fb_point or "Attendance Commendation" in fb_point:
            st.success(fb_point)
        else:
            st.info(fb_point)

    # Full Formatted HTML Report Card Preview
    with st.expander("View Template Schema (Official Institutional Layout)", expanded=False):
        st.caption("This layout reflects the decoupled template structure used to compile both the web representation and the vector PDF document:")
        html_preview = render_html_report_preview(rep, DEFAULT_REPORT_CONFIG)
        st.markdown(html_preview, unsafe_allow_html=True)
