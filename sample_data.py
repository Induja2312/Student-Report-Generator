"""
sample_data.py
==============
Provides realistic sample student datasets for rapid demonstration
during academic presentations and testing.
"""

SAMPLE_STUDENTS = {
    "Aarav Sharma (High Achiever - Excellent)": {
        "name": "Aarav Sharma",
        "roll_no": "24CS801",
        "department": "Computer Science & Engineering",
        "semester": "Semester III",
        "attendance": 94.5,
        "subjects": {
            "Advanced Python Programming": 95,
            "Data Structures & Algorithms": 89,
            "Database Management Systems": 92,
            "Machine Learning Foundations": 96,
            "Web Technologies": 88
        }
    },
    "Priya Patel (Consistent Performer - Good)": {
        "name": "Priya Patel",
        "roll_no": "24CS814",
        "department": "Artificial Intelligence & Data Science",
        "semester": "Semester III",
        "attendance": 84.0,
        "subjects": {
            "Advanced Python Programming": 82,
            "Data Structures & Algorithms": 74,
            "Database Management Systems": 79,
            "Machine Learning Foundations": 85,
            "Web Technologies": 70
        }
    },
    "Rohan Verma (Moderate Performer - Average)": {
        "name": "Rohan Verma",
        "roll_no": "24IT832",
        "department": "Information Technology",
        "semester": "Semester III",
        "attendance": 76.5,
        "subjects": {
            "Advanced Python Programming": 62,
            "Data Structures & Algorithms": 58,
            "Database Management Systems": 67,
            "Machine Learning Foundations": 54,
            "Web Technologies": 59
        }
    },
    "Sneha Rao (Needs Academic Support & Attendance Shortage)": {
        "name": "Sneha Rao",
        "roll_no": "24SE845",
        "department": "Software Engineering",
        "semester": "Semester III",
        "attendance": 61.0,
        "subjects": {
            "Advanced Python Programming": 52,
            "Data Structures & Algorithms": 44,
            "Database Management Systems": 48,
            "Machine Learning Foundations": 42,
            "Web Technologies": 50
        }
    }
}

DEFAULT_SUBJECT_NAMES = [
    "Advanced Python Programming",
    "Data Structures & Algorithms",
    "Database Management Systems",
    "Machine Learning Foundations",
    "Web Technologies"
]

DEPARTMENTS = [
    "Computer Science & Engineering",
    "Artificial Intelligence & Data Science",
    "Information Technology",
    "Software Engineering",
    "Data Analytics & Computational Science"
]

SEMESTERS = [
    "Semester I",
    "Semester II",
    "Semester III",
    "Semester IV"
]
