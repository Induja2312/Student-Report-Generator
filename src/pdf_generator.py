"""
pdf_generator.py
================
Generates professional, printable PDF performance reports using ReportLab Platypus.
Includes student profile, tabular coursework breakdown, embedded Matplotlib chart,
rule-based personalized appraisal, and official verification signature blocks.
"""

import io
from datetime import datetime
from typing import Dict, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether
)

try:
    from reportlab.platypus import HRFlowable
except ImportError:
    try:
        from reportlab.platypus.flowables import HRFlowable
    except ImportError:
        HRFlowable = None



def get_category_color(category: str) -> colors.Color:
    """Returns a ReportLab color corresponding to performance category."""
    if category == "Excellent":
        return colors.HexColor("#10B981")  # Emerald
    elif category == "Good":
        return colors.HexColor("#3B82F6")  # Blue
    elif category == "Average":
        return colors.HexColor("#F59E0B")  # Amber
    else:
        return colors.HexColor("#EF4444")  # Red


def generate_pdf_report(
    processed_data: Dict[str, Any],
    chart_image_bytes: bytes,
    institution_config: Dict[str, Any] = None
) -> bytes:
    """
    Builds an academic performance report PDF and returns raw bytes.

    Args:
        processed_data: Processed student details and computed statistics.
        chart_image_bytes: PNG bytes of the Matplotlib performance chart.
        institution_config: Optional branding dictionary.

    Returns:
        bytes: Complete binary PDF document.
    """
    if institution_config is None:
        institution_config = {
            "institution_name": "INSTITUTE OF ADVANCED STUDIES & RESEARCH",
            "department_label": "Department of Computer Science & Applications",
            "report_title": "STUDENT ACADEMIC PERFORMANCE & APPRAISAL REPORT",
            "academic_year": "Academic Year 2025–2026",
        }

    buffer = io.BytesIO()

    # Printable width: A4 width is 595.27 pt. Margins = 36 pt each. Printable width = 523.27 pt.
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
        title="Student Academic Performance Report",
        author="Automated Report Engine"
    )

    printable_width = 523.0
    story = []

    # Setup styles
    sample_styles = getSampleStyleSheet()

    # Custom Paragraph Styles
    style_inst = ParagraphStyle(
        name="InstHeader",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=1,  # Center
        textColor=colors.HexColor("#475569")
    )
    style_title = ParagraphStyle(
        name="RepTitle",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        alignment=1,  # Center
        textColor=colors.HexColor("#0F172A")
    )
    style_sub = ParagraphStyle(
        name="RepSub",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        alignment=1,  # Center
        textColor=colors.HexColor("#64748B")
    )
    style_cell = ParagraphStyle(
        name="CellText",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )
    style_cell_bold = ParagraphStyle(
        name="CellBold",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A")
    )
    style_th = ParagraphStyle(
        name="THText",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=1,  # Center
        textColor=colors.white
    )
    style_fb_title = ParagraphStyle(
        name="FBTitle",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E40AF")
    )
    style_fb_body = ParagraphStyle(
        name="FBBody",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )
    style_footer_label = ParagraphStyle(
        name="FootLabel",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        alignment=1,  # Center
        textColor=colors.HexColor("#475569")
    )

    student = processed_data["student_info"]
    metrics = processed_data["metrics"]
    feedback = processed_data["feedback"]
    subjects = processed_data["subjects"]
    report_date = datetime.now().strftime("%B %d, %Y")

    # ---------------------------------------------------------
    # 1. Header Section
    # ---------------------------------------------------------
    story.append(Paragraph(institution_config["institution_name"].upper(), style_inst))
    story.append(Spacer(1, 3))
    story.append(Paragraph(institution_config["report_title"], style_title))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        f"{institution_config['academic_year']} &bull; Generated on: {report_date} &bull; Official Transcript Preview",
        style_sub
    ))
    if HRFlowable is not None:
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4F46E5"), spaceAfter=12))
    else:
        divider = Table([[""]], colWidths=[printable_width], rowHeights=[2], style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#4F46E5")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ])
        story.append(divider)
        story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # 2. Student Profile Table
    # ---------------------------------------------------------
    att_val = student["attendance"]
    att_display = f"{att_val:.1f}% ({student['attendance_status']})"

    profile_data = [
        [
            Paragraph("<b>Student Name:</b>", style_cell),
            Paragraph(student["name"], style_cell_bold),
            Paragraph("<b>Roll Number:</b>", style_cell),
            Paragraph(student["roll_no"], style_cell_bold)
        ],
        [
            Paragraph("<b>Department:</b>", style_cell),
            Paragraph(student["department"], style_cell),
            Paragraph("<b>Semester:</b>", style_cell),
            Paragraph(student["semester"], style_cell)
        ],
        [
            Paragraph("<b>Attendance:</b>", style_cell),
            Paragraph(att_display, style_cell_bold),
            Paragraph("<b>Academic Status:</b>", style_cell),
            Paragraph("Regular Enrolled", style_cell)
        ]
    ]

    profile_table = Table(
        profile_data,
        colWidths=[90, 171, 90, 172],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]
    )
    story.append(profile_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # 3. Key Performance Summary Tiles (Table)
    # ---------------------------------------------------------
    cat_color = get_category_color(metrics["category"])

    metrics_table_data = [
        [
            Paragraph("<font size='7' color='#64748B'><b>TOTAL MARKS</b></font><br/><b><font size='12' color='#0F172A'>"
                      f"{metrics['total_marks']}</font></b> <font size='8' color='#64748B'>/ {metrics['max_marks']}</font>", style_cell),
            Paragraph("<font size='7' color='#64748B'><b>AGGREGATE %</b></font><br/><b><font size='12' color='#4F46E5'>"
                      f"{metrics['percentage']:.1f}%</font></b>", style_cell),
            Paragraph(f"<font size='7' color='#64748B'><b>CATEGORY</b></font><br/><b><font size='11' color='{metrics['category_color']}'>"
                      f"{metrics['category']}</font></b>", style_cell),
            Paragraph("<font size='7' color='#64748B'><b>BEST SUBJECT</b></font><br/>"
                      f"<b><font size='9' color='#0F172A'>{metrics['highest_subject'][0]}</font></b> "
                      f"<font size='8' color='#10B981'>({metrics['highest_subject'][1]:.0f})</font>", style_cell),
        ]
    ]

    metrics_table = Table(
        metrics_table_data,
        colWidths=[120, 110, 130, 163],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]
    )
    story.append(metrics_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # 4. Coursework Marks Table
    # ---------------------------------------------------------
    # Header Row
    marks_table_data = [
        [
            Paragraph("Subject Course Title", style_th),
            Paragraph("Max Marks", style_th),
            Paragraph("Marks Scored", style_th),
            Paragraph("Percentage", style_th),
            Paragraph("Letter Grade", style_th),
            Paragraph("Status", style_th),
        ]
    ]

    for idx, (sub_name, mark) in enumerate(subjects.items(), start=1):
        m = float(mark)
        pct = f"{(m / 100.0) * 100:.1f}%"
        from src.data_processor import calculate_grade
        grade = calculate_grade(m)
        status_str = "Pass" if m >= 50 else "Re-Appear"
        status_color = "#166534" if m >= 50 else "#991B1B"

        marks_table_data.append([
            Paragraph(f"{idx}. {sub_name}", style_cell),
            Paragraph("100", ParagraphStyle("C", parent=style_cell, alignment=1)),
            Paragraph(f"<b>{m:.1f}</b>", ParagraphStyle("C", parent=style_cell, alignment=1)),
            Paragraph(pct, ParagraphStyle("C", parent=style_cell, alignment=1)),
            Paragraph(grade, ParagraphStyle("C", parent=style_cell, alignment=1)),
            Paragraph(f"<b><font color='{status_color}'>{status_str}</font></b>", ParagraphStyle("C", parent=style_cell, alignment=1)),
        ])

    # Summary Row
    marks_table_data.append([
        Paragraph("<b>Grand Total / Average</b>", style_cell_bold),
        Paragraph(f"<b>{metrics['max_marks']}</b>", ParagraphStyle("C", parent=style_cell_bold, alignment=1)),
        Paragraph(f"<b>{metrics['total_marks']:.1f}</b>", ParagraphStyle("C", parent=style_cell_bold, alignment=1)),
        Paragraph(f"<b>{metrics['percentage']:.1f}%</b>", ParagraphStyle("C", parent=style_cell_bold, alignment=1)),
        Paragraph(f"<b>Avg: {metrics['average_marks']:.1f}</b>", ParagraphStyle("C", parent=style_cell_bold, alignment=1)),
        Paragraph(f"<b><font color='{metrics['category_color']}'>{metrics['category']}</font></b>", ParagraphStyle("C", parent=style_cell_bold, alignment=1)),
    ])

    course_table = Table(
        marks_table_data,
        colWidths=[183, 60, 70, 70, 75, 65],
        style=[
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F1F5F9")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F8FAFC")]),
        ]
    )
    story.append(course_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # 5. Embedded Performance Chart
    # ---------------------------------------------------------
    if chart_image_bytes:
        chart_buf = io.BytesIO(chart_image_bytes)
        # 515 width, 175 height fits cleanly
        chart_img = Image(chart_buf, width=515, height=175)
        story.append(chart_img)
        story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # 6. Personalized Feedback Section
    # ---------------------------------------------------------
    feedback_paragraphs = [
        Paragraph("<b>📋 Personalized Academic Appraisal & Advisor Feedback</b>", style_fb_title),
        Spacer(1, 4)
    ]
    for fb in feedback:
        feedback_paragraphs.append(
            Paragraph(f"&bull;&nbsp;&nbsp;{fb}", style_fb_body)
        )
        feedback_paragraphs.append(Spacer(1, 2))

    feedback_container = Table(
        [[feedback_paragraphs]],
        colWidths=[523],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0FDF4") if metrics["category"] == "Excellent" else colors.HexColor("#EFF6FF")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#86EFAC") if metrics["category"] == "Excellent" else colors.HexColor("#BFDBFE")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )

    # ---------------------------------------------------------
    # 7. Official Signatures Block
    # ---------------------------------------------------------
    sig_data = [
        [
            Paragraph("________________________<br/><b>Class Advisor</b><br/><font size='7' color='#64748B'>Signature & Date</font>", style_footer_label),
            Paragraph("________________________<br/><b>Head of Department</b><br/><font size='7' color='#64748B'>Department Seal & Date</font>", style_footer_label),
            Paragraph("________________________<br/><b>Dean of Academics</b><br/><font size='7' color='#64748B'>Academic Council</font>", style_footer_label),
        ]
    ]
    sig_table = Table(
        sig_data,
        colWidths=[174, 174, 175],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )

    # Keep feedback and signatures together to prevent awkward page splits
    story.append(KeepTogether([
        feedback_container,
        Spacer(1, 14),
        sig_table
    ]))

    # Build the document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
