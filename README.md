# Personalized Report Generation using Templates and Python

An automated, template-driven academic performance appraisal and PDF report generation web application built with **Python 3**, **Streamlit**, **Pandas**, **Matplotlib**, and **ReportLab Platypus**.

Developed for the **Advanced Python Programming** postgraduate presentation.

---

## 📌 Project Overview

Generating personalized academic report cards manually is time-consuming and error-prone. This application automates the entire lifecycle:
1. **Interactive Data Input & Validation:** Collects student information and subject scores with strict validation checks (0–100 limits, required fields).
2. **Dynamic Data Processing:** Computes total marks, averages, aggregate percentages, identifies highest/lowest subjects, and assigns academic standing categories using well-defined thresholds.
3. **Automated Personalized Feedback:** Rule-driven expert feedback engine generating customized commendations, targeted remedial advice, and attendance warnings.
4. **Data Visualization:** Generates publication-ready comparative bar charts with average reference lines using Matplotlib.
5. **Decoupled Template Rendering:** Visualizes reports in modern HTML/CSS and compiles vector-quality, printable PDF documents via ReportLab Platypus.

---

## 🛠️ Technology Stack (100% Free & Open-Source)

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core programming language & logic |
| **Streamlit** | Interactive web application user interface |
| **Pandas** | Tabular data structures & statistical summaries |
| **Matplotlib** | Academic comparative bar charts & visual analytics |
| **ReportLab** | Vector PDF report generation with embedded charts & tables |

> 🔒 **Zero External Costs:** Requires **no** paid APIs, **no** database setup, and **no** machine learning models. Operates entirely offline and locally.

---

## 📂 Project Directory Structure

```text
assignment/
├── app.py                      # Main Streamlit web application
├── sample_data.py              # Pre-configured student profiles for instant demo
├── requirements.txt            # Dependency specification
├── README.md                   # Complete documentation and setup manual
├── PRESENTATION_GUIDE.md       # 5-minute presentation script & Viva FAQ
└── src/
    ├── __init__.py             # Package initializer
    ├── data_processor.py       # Data validation, calculations & feedback rules
    ├── visualizer.py           # Matplotlib bar chart creation & PNG byte export
    ├── pdf_generator.py        # ReportLab Platypus PDF compilation engine
    └── template_engine.py      # Reusable template layout & HTML preview
```

---

## 🚀 Step-by-Step Setup Instructions (Windows)

Follow these exact steps in **Windows PowerShell** or **Command Prompt**:

### Step 1: Open Terminal in Project Folder
Open your terminal and ensure you are in the project directory:
```powershell
cd "d:\College\PG\SEM III\Python\assignment"
```

### Step 2: Create a Python Virtual Environment
Creating a virtual environment isolates your dependencies from global Python installations:
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- **In PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If you see an execution policy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` and then re-run the activation command).*
- **Or in Command Prompt (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
You will see `(venv)` appear at the start of your terminal prompt.

### Step 4: Install Dependencies
Upgrade pip and install the required libraries:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Run the Streamlit Application
Launch the web interface:
```powershell
streamlit run app.py
```
Streamlit will automatically open your default browser at `http://localhost:8501`.

### Step 6: Test with Sample Data
1. Look at the left sidebar under **"Classroom Demo Presets"**.
2. Select a profile (e.g. *Aarav Sharma* or *Priya Patel*) and click **"Load Profile into Form"**.
3. Notice how all inputs (Name, Roll No, Department, Attendance, Marks) populate automatically.
4. Click the **"🚀 Generate Personalized Report"** button.

### Step 7: Generate & Download PDF
1. Switch to the **"📊 2. Generated Report & Download PDF"** tab.
2. Inspect the live metrics, the Matplotlib bar chart, and the personalized recommendations.
3. Click the blue **"📥 Download PDF Report"** button at the top right to download the generated PDF.

---

## 📏 Academic Evaluation Logic & Thresholds

### 1. Performance Categories
| Category | Aggregate Percentage | Action / Rationale |
| :--- | :--- | :--- |
| **Excellent** | $\ge 85\%$ | Outstanding mastery across curriculum; honors commendation. |
| **Good** | $70\% - 84.99\%$ | Commendable consistency; high potential for top tier. |
| **Average** | $50\% - 69.99\%$ | Meets university passing benchmark; daily revision recommended. |
| **Needs Improvement** | $< 50\%$ | Below benchmark; departmental mentoring & remedial work advised. |

### 2. Attendance Benchmark
- **$\ge 75\%$:** Marked as **Satisfactory** (Meets mandatory academic eligibility).
- **$< 75\%$:** Triggers an **Attendance Shortage Warning** per standard university norms.

---

## 📄 Generated PDF Features
The downloaded PDF report includes:
- **Institution Header & Report Metadata:** Standardized academic title, academic year, and timestamp.
- **Student Profile Table:** Name, Roll Number, Department, Semester, Attendance.
- **Key Summary Cards:** Total Marks, Percentage, Performance Category badge.
- **Coursework Breakdown Table:** Max Marks, Marks Obtained, Percentage, Letter Grade, and Pass/Re-Appear status.
- **Embedded Visual Analytics:** Matplotlib chart crisply scaled with passing line and student average.
- **Personalized Academic Appraisal:** Bulleted recommendations customized to the student's highest/lowest subjects.
- **Official Signature Blocks:** Class Advisor, Head of Department, and Dean of Academics lines.

---

## 🌐 Deploying to Render (Free Web Service)

This repository is pre-configured for instant deployment on [Render](https://render.com).

### Quick Deployment Settings:
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- **Free Tier Plan:** Available

