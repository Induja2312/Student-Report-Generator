"""
app.py
======
Main Streamlit Web Application:
"Personalized Report Generation using Templates and Python"

Postgraduate Coursework - Advanced Python Programming
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
    page_title="Personalized Report Generation using Templates and Python",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern warm cream academic dashboard styling
st.markdown("""
<style>
    /* Warm Cream Background for Entire Application */
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
    }
    .main-header p {
        font-size: 14px;
        color: #DBCAB7 !important;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* High Visibility Typography on Cream Canvas */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p {
        color: #2A201A !important;
    }
    .main-header h1, .main-header p, .stButton > button, .stDownloadButton > button {
        color: #FFFFFF !important;
    }

    /* Metric Badges */
    .metric-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
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
    }
    div[data-testid="stMetricValue"] div {
        color: #2A201A !important;
        font-weight: 800 !important;
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

    /* Buttons in Warm Mahogany */
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        background-color: #8B4513 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #A0522D !important;
        color: #FFFFFF !important;
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
        width=48
    )
    st.markdown("### 🎓 Classroom Demo Presets")
    st.caption("Select a sample student profile to populate the form instantly for your presentation:")

    chosen_preset = st.selectbox(
        "Choose Demonstration Profile:",
        options=list(SAMPLE_STUDENTS.keys()),
        index=0
    )

    if st.button("📥 Load Profile into Form", use_container_width=True):
        load_preset(chosen_preset)
        st.toast(f"Loaded {chosen_preset.split('(')[0].strip()}'s profile!", icon="✅")

    st.markdown("---")
    st.markdown("### ⚙️ System Technology Stack")
    st.markdown("""
    - **Language:** Python 3
    - **UI Engine:** Streamlit
    - **Data Pipeline:** Pandas
    - **Visualization:** Matplotlib
    - **Document Engine:** ReportLab Platypus
    - **Architecture:** Decoupled Template Pattern
    """)

    st.markdown("---")
    st.markdown("### 📏 Grading Thresholds")
    st.markdown("""
    * **Excellent:** $\ge 85\%$
    * **Good:** $70\% - 84.9\%$
    * **Average:** $50\% - 69.9\%$
    * **Needs Improvement:** $< 50\%$
    * **Attendance Standard:** $\ge 75\%$
    """)


# -----------------------------------------------------------------------------
# 4. Main Page Header
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>Personalized Report Generation using Templates and Python</h1>
    <p>Advanced Python Programming Coursework &bull; Automated Academic Appraisal & PDF Generation System</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Two-Tab Layout: [1] Student Input Form | [2] Live Report & PDF
# -----------------------------------------------------------------------------
tab_input, tab_preview = st.tabs(["📝 1. Student Information & Marks Input", "📊 2. Generated Report & Download PDF"])

with tab_input:
    st.markdown("#### Enter Student Academic Records")
    st.info("💡 **Presentation Tip:** You can quickly load sample profiles from the sidebar or manually adjust any value below.")

    with st.form("student_input_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 👤 Student Identification")
            name_input = st.text_input(
                "Full Name:",
                value=st.session_state.name_val,
                placeholder="e.g. Induja",
                help="Enter student's official full name."
            )
            roll_input = st.text_input(
                "Roll Number / Registration ID:",
                value=st.session_state.roll_val,
                placeholder="e.g. 25MX101",
                help="Unique student identification number."
            )
            dept_input = st.selectbox(
                "Academic Department (Recommended: MCA):",
                options=DEPARTMENTS,
                index=DEPARTMENTS.index(st.session_state.dept_val) if st.session_state.dept_val in DEPARTMENTS else 0
            )

        with col2:
            st.markdown("##### 📅 Enrollment & Attendance")
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
        st.markdown("##### 📚 Subject Coursework Marks (Out of 100)")

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
        generate_clicked = st.form_submit_button("🚀 Generate Personalized Report", use_container_width=True, type="primary")

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
            st.error("❌ **Validation Failed:** Please resolve the following errors before proceeding:")
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
            with st.spinner("Processing marks, applying appraisal rules, and generating graphics..."):
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

            st.success("✅ **Report Successfully Generated!** Check the 'Generated Report & Download PDF' tab to review and download.")


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
        st.markdown(f"### 📋 Report Preview: **{student['name']}** ({student['roll_no']})")
    with col_btn:
        safe_name = student["name"].replace(" ", "_")
        pdf_filename = f"Performance_Report_{safe_name}_{student['roll_no']}.pdf"
        st.download_button(
            label="📥 Download PDF Report",
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
        st.markdown("##### 📊 Comparative Performance Chart")
        st.pyplot(st.session_state.chart_fig, use_container_width=True)

    with c_table:
        st.markdown("##### 📑 Subject-wise Performance Summary")
        df_display = rep["dataframe"][["Subject Name", "Marks Obtained", "Grade", "Status"]]
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("##### 🎯 Academic Highlights")
        st.markdown(f"- **Top Subject:** `{metrics['highest_subject'][0]}` ({metrics['highest_subject'][1]:.0f}/100)")
        st.markdown(f"- **Lowest Subject:** `{metrics['lowest_subject'][0]}` ({metrics['lowest_subject'][1]:.0f}/100)")
        st.markdown(f"- **Category Rationale:** {metrics['category_desc']}")

    st.markdown("---")

    # Personalized Feedback Callout
    st.markdown("##### 💬 Personalized Academic Feedback & Recommendations")
    for fb_point in rep["feedback"]:
        if "⚠️" in fb_point:
            st.warning(fb_point)
        elif "🌟" in fb_point or "🏆" in fb_point:
            st.success(fb_point)
        else:
            st.info(fb_point)

    # Full Formatted HTML Report Card Preview
    with st.expander("🔍 View Pre-Rendered Template Layout (Official Format)", expanded=False):
        st.caption("This layout reflects the decoupled template structure used to compile both the web representation and the vector PDF document:")
        html_preview = render_html_report_preview(rep, DEFAULT_REPORT_CONFIG)
        st.markdown(html_preview, unsafe_allow_html=True)
