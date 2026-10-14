# Academic Presentation Deck: Personalized Report Generation using Templates and Python

This directory contains the presentation programs and slides for the **Advanced Python Programming** coursework project.

---

## 🎨 Theme & Typography Standards

As requested, all slides strictly adhere to the following specifications:
* **Slide Count:** Exactly 10 slides.
* **Canvas Background:** Pure White (`#FFFFFF`).
* **Theme Accents:** Dark Imperial Purple (`#3B0764`), Deep Royal Purple (`#581C87`), and Vibrant Purple Highlights (`#7E22CE`).
* **Title Font Size:** **35 pt** (bold, dark purple).
* **Subtitle Font Size:** **25 pt** (bold, deep purple).
* **Text / Body Font Size:** **20 pt** (dark purple-navy high-contrast text).
* **Embedded Graphics:** 4 high-resolution architectural diagrams and analytics charts.

---

## 📂 Presentation Folder Contents

```text
presentation/
├── generate_presentation.py      # Python script that generates the .pptx presentation
├── presentation_slides.html      # Interactive 10-slide HTML presentation deck
├── requirements_presentation.txt # Dependencies for PPTX generator
├── README.md                     # Presentation user guide
└── images/                       # Generated architectural & chart graphics
    ├── pipeline_architecture.png
    ├── performance_chart.png
    ├── threshold_scale.png
    └── pdf_mockup.png
```

---

## 🚀 How to Use & Present

You have **two flexible ways** to present:

### Option 1: Generate & Open PowerPoint (.pptx) File
If you have Microsoft PowerPoint, Google Slides, or LibreOffice installed:

1. In your terminal, activate your virtual environment:
   ```powershell
   cd "d:\College\PG\SEM III\Python\assignment"
   .\venv\Scripts\Activate.ps1
   ```
2. Install presentation requirements:
   ```powershell
   pip install -r presentation\requirements_presentation.txt
   ```
3. Run the generator script:
   ```powershell
   python presentation\generate_presentation.py
   ```
4. This will create:
   `presentation\personalized_report_presentation.pptx`
   Double-click to open and present directly in PowerPoint!

---

### Option 2: Present Directly in Any Browser (Zero Install)
You can immediately present without running any script or installing PowerPoint:

1. Navigate to:  
   `d:\College\PG\SEM III\Python\assignment\presentation\`
2. Double-click [presentation_slides.html](file:///d:/College/PG/SEM%20III/Python/assignment/presentation/presentation_slides.html) to open it in **Google Chrome**, **Microsoft Edge**, or **Firefox**.
3. **Interactive Features:**
   * **Next Slide:** Press `Right Arrow`, `Spacebar`, or click **Next →**.
   * **Previous Slide:** Press `Left Arrow` or click **← Previous**.
   * **Fullscreen Mode:** Click the **⛶ Fullscreen** button for a full-screen classroom presentation.
   * **Export to PDF:** Click **🖨 Print / Save as PDF** (`Ctrl + P`) and select *Landscape* orientation.

---

## 📑 10-Slide Outline Overview

1. **Slide 1:** Title Slide (Project Title, Subtitle, Academic Credentials & Architecture).
2. **Slide 2:** Problem Statement & Academic Motivation (Manual spreadsheet bottlenecks & lack of feedback).
3. **Slide 3:** Proposed Solution & Key Objectives (Zero-cost, template-driven automation).
4. **Slide 4:** System Architecture & Processing Pipeline (4-Stage ingestion, processing, analytics, PDF).
5. **Slide 5:** Technology Stack & Technical Rationale (Streamlit, Pandas, Matplotlib, ReportLab Platypus).
6. **Slide 6:** Input Validation & Categorization (0–100 boundary rules, 4 grading tiers & attendance criteria).
7. **Slide 7:** Dynamic Data Visualization Engine (In-memory Matplotlib Agg bar chart with benchmark lines).
8. **Slide 8:** Template Decoupling & Vector PDF Generation (Decoupled layout, Platypus flowables & zero disk clutter).
9. **Slide 9:** Demonstration & User Interface Workflow (1-Click presets, live metric cards & PDF export).
10. **Slide 10:** Conclusion, Future Scope & Viva Discussion (Batch CSV scaling, LMS integration & Q&A).
