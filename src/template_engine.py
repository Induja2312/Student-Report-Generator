"""
template_engine.py
==================
Defines the reusable academic report template structure and handles
data interpolation for web preview rendering.
Decouples visual layout from dynamic data processing.
"""

from typing import Dict, Any
from datetime import datetime


# Standard Institution & Report Metadata Template
DEFAULT_REPORT_CONFIG = {
    "institution_name": "INSTITUTE OF ADVANCED STUDIES & RESEARCH",
    "department_label": "Department of Computer Applications (MCA)",
    "report_title": "STUDENT ACADEMIC PERFORMANCE & APPRAISAL REPORT",
    "academic_year": "Academic Year 2025–2026",
    "grading_scale": "Absolute Grading System (Scale 0–100)"
}


def render_html_report_preview(processed_data: Dict[str, Any], config: Dict[str, Any] = None) -> str:
    """
    Renders an interactive, styled HTML preview of the report
    using predefined CSS layout templates and dynamic data injection.

    Args:
        processed_data: Output dictionary from data_processor.process_student_data().
        config: Institution branding configuration dictionary.

    Returns:
        HTML string suitable for rendering in Streamlit via st.markdown(..., unsafe_allow_html=True).
    """
    if config is None:
        config = DEFAULT_REPORT_CONFIG

    student = processed_data["student_info"]
    metrics = processed_data["metrics"]
    feedback = processed_data["feedback"]
    subjects = processed_data["subjects"]
    report_date = datetime.now().strftime("%B %d, %Y")

    # Feedback points HTML
    feedback_items_html = "".join([
        f"<li style='margin-bottom: 8px; color: #2A201A; line-height: 1.5;'>{fb}</li>"
        for fb in feedback
    ])

    # Table rows HTML
    table_rows_html = ""
    for sub_name, mark in subjects.items():
        m = float(mark)
        status_badge = (
            "<span style='background:#DCFCE7; color:#166534; padding:3px 8px; border-radius:12px; font-weight:700; font-size:11px;'>PASS</span>"
            if m >= 50
            else "<span style='background:#FEE2E2; color:#991B1B; padding:3px 8px; border-radius:12px; font-weight:700; font-size:11px;'>RE-APPEAR</span>"
        )
        bar_width = min(100, max(0, int(m)))
        bar_color = "#10B981" if m >= 85 else ("#3B82F6" if m >= 70 else ("#F59E0B" if m >= 50 else "#EF4444"))

        table_rows_html += f"""
        <tr style='border-bottom: 1px solid #EFE6D7;'>
            <td style='padding: 10px 14px; font-weight: 600; color: #2A201A;'>{sub_name}</td>
            <td style='padding: 10px 14px; text-align: center; color: #6B5848;'>100</td>
            <td style='padding: 10px 14px; text-align: center; font-weight: 700; color: #2A201A;'>{m:.1f}</td>
            <td style='padding: 10px 14px;'>
                <div style='background: #E8DFD3; border-radius: 6px; height: 8px; width: 100%; overflow: hidden;'>
                    <div style='background: {bar_color}; width: {bar_width}%; height: 100%; border-radius: 6px;'></div>
                </div>
            </td>
            <td style='padding: 10px 14px; text-align: center;'>{status_badge}</td>
        </tr>
        """

    # Attendance warning styling
    att_color = "#15803D" if student["attendance"] >= 75 else "#DC2626"
    att_bg = "#ECFDF5" if student["attendance"] >= 75 else "#FEF2F2"

    html_template = f"""
    <div style='background: #FFFDF9; border: 1px solid #E8DFD3; border-radius: 12px; padding: 26px; box-shadow: 0 4px 14px rgba(70, 50, 30, 0.06); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;'>
        <!-- Report Header -->
        <div style='text-align: center; border-bottom: 2px solid #E5DACB; padding-bottom: 16px; margin-bottom: 20px;'>
            <div style='font-size: 13px; font-weight: 800; letter-spacing: 1.5px; color: #6B5848; text-transform: uppercase;'>{config["institution_name"]}</div>
            <div style='font-size: 21px; font-weight: 800; color: #2A201A; margin: 4px 0 2px 0;'>{config["report_title"]}</div>
            <div style='font-size: 13px; color: #7A695A;'>{config["department_label"]} &bull; {config["academic_year"]} &bull; Issued: {report_date}</div>
        </div>

        <!-- Student Profile Card -->
        <div style='background: #FAF7EE; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px; border-left: 5px solid #8B4513; border: 1px solid #E5DACB; border-left-width: 5px;'>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px;'>
                <div><span style='color: #6B5848; font-size: 12px; display: block; font-weight: 600;'>Student Full Name</span><strong style='color: #2A201A; font-size: 16px;'>{student["name"]}</strong></div>
                <div><span style='color: #6B5848; font-size: 12px; display: block; font-weight: 600;'>Roll Number</span><strong style='color: #2A201A; font-size: 16px;'>{student["roll_no"]}</strong></div>
                <div><span style='color: #6B5848; font-size: 12px; display: block; font-weight: 600;'>Department</span><strong style='color: #2A201A; font-size: 16px;'>{student["department"]}</strong></div>
                <div><span style='color: #6B5848; font-size: 12px; display: block; font-weight: 600;'>Semester</span><strong style='color: #2A201A; font-size: 16px;'>{student["semester"]}</strong></div>
                <div><span style='color: #6B5848; font-size: 12px; display: block; font-weight: 600;'>Attendance Record</span>
                    <span style='display: inline-block; background: {att_bg}; color: {att_color}; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-size: 13px; margin-top: 2px;'>
                        {student["attendance"]:.1f}% ({student["attendance_status"]})
                    </span>
                </div>
            </div>
        </div>

        <!-- Key Metrics Cards -->
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; margin-bottom: 22px;'>
            <div style='background: #FAF7EE; border: 1px solid #E5DACB; border-radius: 8px; padding: 14px; text-align: center;'>
                <div style='font-size: 11px; color: #6B5848; font-weight: 700; text-transform: uppercase;'>Total Marks</div>
                <div style='font-size: 20px; font-weight: 800; color: #2A201A; margin-top: 4px;'>{metrics["total_marks"]} <span style='font-size: 12px; font-weight: 600; color: #7A695A;'>/ {metrics["max_marks"]}</span></div>
            </div>
            <div style='background: #FAF7EE; border: 1px solid #E5DACB; border-radius: 8px; padding: 14px; text-align: center;'>
                <div style='font-size: 11px; color: #6B5848; font-weight: 700; text-transform: uppercase;'>Aggregate %</div>
                <div style='font-size: 20px; font-weight: 800; color: #8B4513; margin-top: 4px;'>{metrics["percentage"]:.1f}%</div>
            </div>
            <div style='background: #FAF7EE; border: 1px solid #E5DACB; border-radius: 8px; padding: 14px; text-align: center;'>
                <div style='font-size: 11px; color: #6B5848; font-weight: 700; text-transform: uppercase;'>Performance</div>
                <div style='display: inline-block; background: {metrics["category_color"]}20; color: {metrics["category_color"]}; font-size: 13px; font-weight: 800; padding: 4px 12px; border-radius: 12px; margin-top: 4px;'>
                    {metrics["category"]}
                </div>
            </div>
            <div style='background: #FAF7EE; border: 1px solid #E5DACB; border-radius: 8px; padding: 14px; text-align: center;'>
                <div style='font-size: 11px; color: #6B5848; font-weight: 700; text-transform: uppercase;'>Best Subject</div>
                <div style='font-size: 13px; font-weight: 700; color: #2A201A; margin-top: 6px;'>{metrics["highest_subject"][0]}</div>
                <div style='font-size: 12px; color: #15803D; font-weight: 800;'>({metrics["highest_subject"][1]:.0f}/100)</div>
            </div>
        </div>

        <!-- Academic Performance Table -->
        <div style='margin-bottom: 22px;'>
            <div style='font-size: 15px; font-weight: 800; color: #2A201A; margin-bottom: 10px;'>Coursework Evaluation</div>
            <table style='width: 100%; border-collapse: collapse; font-size: 13.5px; background: #FFFDF9; border: 1px solid #E5DACB; border-radius: 8px; overflow: hidden;'>
                <thead>
                    <tr style='background: #F3EDE2; color: #3A2A1E; text-align: left; font-size: 12px; text-transform: uppercase; font-weight: 700;'>
                        <th style='padding: 11px 14px;'>Subject</th>
                        <th style='padding: 11px 14px; text-align: center;'>Max</th>
                        <th style='padding: 11px 14px; text-align: center;'>Marks</th>
                        <th style='padding: 11px 14px; width: 30%;'>Score Distribution</th>
                        <th style='padding: 11px 14px; text-align: center;'>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>

        <!-- Personalized Appraisal & Recommendations -->
        <div style='background: #FFFBF0; border: 1px solid #F3DEB0; border-radius: 8px; padding: 18px 22px; margin-bottom: 20px;'>
            <div style='font-size: 15px; font-weight: 800; color: #854D0E; margin-bottom: 10px;'>
                📋 Personalized Appraisal & Recommendations
            </div>
            <ul style='margin: 0; padding-left: 20px; font-size: 13.5px;'>
                {feedback_items_html}
            </ul>
        </div>

        <!-- Verification Signature Block -->
        <div style='display: flex; justify-content: space-between; margin-top: 32px; padding-top: 16px; border-top: 1px dashed #D6C8B5; color: #6B5848; font-size: 12px;'>
            <div style='text-align: center;'>
                <div style='width: 160px; border-bottom: 1px solid #8C7A6B; margin-bottom: 4px; height: 28px;'></div>
                <strong style='color: #2A201A;'>Class Advisor</strong>
            </div>
            <div style='text-align: center;'>
                <div style='width: 160px; border-bottom: 1px solid #8C7A6B; margin-bottom: 4px; height: 28px;'></div>
                <strong style='color: #2A201A;'>Head of Department (MCA)</strong>
            </div>
            <div style='text-align: center;'>
                <div style='width: 160px; border-bottom: 1px solid #8C7A6B; margin-bottom: 4px; height: 28px;'></div>
                <strong style='color: #2A201A;'>Dean of Academics</strong>
            </div>
        </div>
    </div>
    """
    return html_template
