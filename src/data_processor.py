"""
data_processor.py
=================
Handles data validation, statistical calculations, performance categorization,
and rule-based personalized feedback generation.
"""

from typing import Dict, List, Tuple, Any
import pandas as pd


def validate_student_inputs(
    name: str,
    roll_no: str,
    department: str,
    semester: str,
    attendance: float,
    subjects: Dict[str, float]
) -> Tuple[bool, List[str]]:
    """
    Validates all inputs provided by the user.

    Returns:
        (is_valid, error_messages): Tuple containing a boolean flag and a list of error strings.
    """
    errors: List[str] = []

    # 1. Student Name validation
    if not name or not name.strip():
        errors.append("Student Name cannot be empty.")
    elif len(name.strip()) < 2:
        errors.append("Student Name must be at least 2 characters long.")

    # 2. Roll Number validation
    if not roll_no or not roll_no.strip():
        errors.append("Roll Number cannot be empty.")

    # 3. Department validation
    if not department or not department.strip():
        errors.append("Department must be selected or specified.")

    # 4. Semester validation
    if not semester or not semester.strip():
        errors.append("Semester must be selected.")

    # 5. Attendance validation (0 to 100)
    try:
        att = float(attendance)
        if att < 0.0 or att > 100.0:
            errors.append("Attendance must be between 0% and 100%.")
    except (ValueError, TypeError):
        errors.append("Attendance must be a valid numeric value.")

    # 6. Subject marks validation (0 to 100 for each subject)
    if not subjects:
        errors.append("At least one subject mark must be provided.")
    else:
        for sub_name, mark in subjects.items():
            try:
                m = float(mark)
                if m < 0.0 or m > 100.0:
                    errors.append(f"Marks for '{sub_name}' must be between 0 and 100 (entered: {mark}).")
            except (ValueError, TypeError):
                errors.append(f"Marks for '{sub_name}' must be a valid numeric value.")

    return (len(errors) == 0, errors)


def assign_performance_category(percentage: float) -> Tuple[str, str, str]:
    """
    Categorizes student performance using clearly defined academic thresholds.

    Thresholds:
      - Excellent:         Percentage >= 85.0%
      - Good:              70.0% <= Percentage < 85.0%
      - Average:           50.0% <= Percentage < 70.0%
      - Needs Improvement: Percentage < 50.0%

    Returns:
        (category_name, color_hex, badge_description)
    """
    if percentage >= 85.0:
        return (
            "Excellent",
            "#10B981",  # Emerald Green
            "Outstanding academic performance demonstrating deep subject mastery."
        )
    elif percentage >= 70.0:
        return (
            "Good",
            "#3B82F6",  # Royal Blue
            "Consistent and commendable performance with strong foundational grasp."
        )
    elif percentage >= 50.0:
        return (
            "Average",
            "#F59E0B",  # Amber / Warm Orange
            "Satisfactory performance meeting course standards; targeted effort recommended."
        )
    else:
        return (
            "Needs Improvement",
            "#EF4444",  # Crimson Red
            "Performance is below expected benchmarks. Academic counseling advised."
        )


def calculate_grade(mark: float) -> str:
    """Helper function to assign a standard letter grade per subject."""
    if mark >= 90:
        return "O (Outstanding)"
    elif mark >= 80:
        return "A+ (Excellent)"
    elif mark >= 70:
        return "A (Very Good)"
    elif mark >= 60:
        return "B+ (Good)"
    elif mark >= 50:
        return "B (Pass)"
    else:
        return "RA (Re-Appear)"


def generate_personalized_feedback(
    name: str,
    category: str,
    percentage: float,
    highest_sub: Tuple[str, float],
    lowest_sub: Tuple[str, float],
    attendance: float
) -> List[str]:
    """
    Generates intelligent, personalized feedback points based on
    the student's marks distribution, highest/lowest subjects, and attendance.
    """
    feedback_points: List[str] = []

    # Point 1: Academic Standing & Category feedback
    if category == "Excellent":
        feedback_points.append(
            f"🌟 Academic Excellence: {name} has demonstrated exemplary mastery across the curriculum "
            f"with an overall aggregate of {percentage:.1f}%. Maintain this stellar momentum."
        )
    elif category == "Good":
        feedback_points.append(
            f"👍 Strong Foundation: {name} shows commendable consistency with a solid aggregate of "
            f"{percentage:.1f}%. With slight refinement in weaker areas, an Excellent grade is well within reach."
        )
    elif category == "Average":
        feedback_points.append(
            f"📈 Steady Progress: {name} meets standard course requirements with {percentage:.1f}%. "
            f"Focusing on structured daily revision will yield substantial score improvements."
        )
    else:
        feedback_points.append(
            f"⚠️ Academic Support Recommended: {name}'s aggregate stands at {percentage:.1f}%. "
            f"We strongly encourage attending departmental mentoring and peer-study workshops."
        )

    # Point 2: Highest-scoring subject (Praise Strength)
    high_name, high_mark = highest_sub
    feedback_points.append(
        f"🏆 Core Strength: Outstanding performance in '{high_name}' with a score of {high_mark:.1f}/100. "
        f"This subject highlights your analytical aptitude."
    )

    # Point 3: Lowest-scoring subject (Targeted Growth Advisory)
    low_name, low_mark = lowest_sub
    if low_mark < 50.0:
        feedback_points.append(
            f"🎯 Urgent Focus Area: Immediate remedial attention is required in '{low_name}' ({low_mark:.1f}/100). "
            f"Consult your course instructor for doubt-clearing and previous semester problem sets."
        )
    elif low_mark < 70.0:
        feedback_points.append(
            f"🎯 Focus Area: Dedicate extra practice hours to '{low_name}' ({low_mark:.1f}/100) "
            f"to boost your overall aggregate further."
        )
    else:
        feedback_points.append(
            f"🎯 Balanced Performance: Even your lowest score is solid at {low_mark:.1f}/100 in '{low_name}'. "
            f"Continuous revision will sustain this balanced performance."
        )

    # Point 4: Attendance Advisory
    if attendance >= 90.0:
        feedback_points.append(
            f"📅 Attendance Commendation: Exemplary class presence of {attendance:.1f}%. "
            f"Regular attendance directly reflects your academic discipline."
        )
    elif attendance >= 75.0:
        feedback_points.append(
            f"📅 Attendance Status: Attendance is satisfactory at {attendance:.1f}% "
            f"(meets university regulation threshold of 75%). Aim to keep it above 85%."
        )
    else:
        feedback_points.append(
            f"⚠️ Attendance Warning: Current attendance is {attendance:.1f}%, which is BELOW "
            f"the mandatory 75% university eligibility requirement. Regularize attendance immediately."
        )

    return feedback_points


def process_student_data(student_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main processing function:
    - Calculates total, average, percentage
    - Determines highest and lowest subjects
    - Produces Pandas DataFrame for tabular representation
    - Assigns performance category and feedback

    Args:
        student_input: Dictionary with keys:
            name, roll_no, department, semester, attendance, subjects

    Returns:
        Structured dictionary containing all computed metrics, summaries, and feedback.
    """
    subjects: Dict[str, float] = student_input["subjects"]
    num_subjects = len(subjects)
    total_marks = sum(subjects.values())
    max_marks = num_subjects * 100
    average_marks = round(total_marks / num_subjects, 2) if num_subjects > 0 else 0.0
    percentage = round((total_marks / max_marks) * 100, 2) if max_marks > 0 else 0.0

    # Identify highest and lowest subjects
    sorted_subjects = sorted(subjects.items(), key=lambda item: item[1], reverse=True)
    highest_subject = sorted_subjects[0] if sorted_subjects else ("None", 0.0)
    lowest_subject = sorted_subjects[-1] if sorted_subjects else ("None", 0.0)

    # Performance category
    category, color_hex, category_desc = assign_performance_category(percentage)

    # Attendance status
    attendance = float(student_input["attendance"])
    attendance_status = "Satisfactory" if attendance >= 75.0 else "Shortage Warning"

    # Personalized feedback
    feedback = generate_personalized_feedback(
        name=student_input["name"],
        category=category,
        percentage=percentage,
        highest_sub=highest_subject,
        lowest_sub=lowest_subject,
        attendance=attendance
    )

    # Create Pandas DataFrame for structured presentation
    records = []
    for sub_name, mark in subjects.items():
        records.append({
            "Subject Name": sub_name,
            "Max Marks": 100,
            "Marks Obtained": round(float(mark), 1),
            "Percentage": f"{(float(mark) / 100.0) * 100:.1f}%",
            "Grade": calculate_grade(float(mark)),
            "Status": "Pass" if float(mark) >= 50.0 else "Needs Review"
        })

    df_marks = pd.DataFrame(records)

    return {
        "student_info": {
            "name": student_input["name"].strip(),
            "roll_no": student_input["roll_no"].strip(),
            "department": student_input["department"].strip(),
            "semester": student_input["semester"].strip(),
            "attendance": attendance,
            "attendance_status": attendance_status,
        },
        "metrics": {
            "total_marks": round(total_marks, 1),
            "max_marks": max_marks,
            "average_marks": average_marks,
            "percentage": percentage,
            "category": category,
            "category_color": color_hex,
            "category_desc": category_desc,
            "highest_subject": highest_subject,
            "lowest_subject": lowest_subject,
            "num_subjects": num_subjects
        },
        "subjects": subjects,
        "dataframe": df_marks,
        "feedback": feedback
    }
