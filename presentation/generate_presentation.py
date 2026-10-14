"""
generate_presentation.py
========================
Automated PowerPoint (.pptx) Presentation Generator for:
"Personalized Report Generation using Templates and Python"

Specifications enforced:
- Exactly 10 Slides
- Slide Title: Font Size 35 pt
- Slide Subtitle: Font Size 25 pt
- Slide Body Text: Font Size 20 pt
- Theme: Dark Purple Accents on Crisp White Background
- Generates and embeds high-resolution architectural & analytical images
"""

import os
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
except ModuleNotFoundError:
    import sys
    import subprocess
    print("=" * 65)
    print("⚠️  Package 'python-pptx' is not yet installed in this environment.")
    print("🚀 Automatically installing 'python-pptx' via pip now...")
    print("=" * 65)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE
        print("✅ Successfully installed python-pptx! Generating presentation now...\n")
    except Exception as err:
        print("\n❌ Could not automatically install python-pptx:", err)
        print("👉 Please manually run this command in your PowerShell terminal:")
        print("    pip install python-pptx\n")
        sys.exit(1)


# -----------------------------------------------------------------------------
# Color Palette Definition (Dark Purple Theme on White Canvas)
# -----------------------------------------------------------------------------
COLOR_WHITE = RGBColor(255, 255, 255)          # Canvas Background
COLOR_DARK_PURPLE = RGBColor(59, 7, 100)       # #3B0764 - Primary Headings / Accents
COLOR_DEEP_PURPLE = RGBColor(88, 28, 135)      # #581C87 - Subtitles / Borders
COLOR_VIBRANT_PURPLE = RGBColor(126, 34, 206)  # #7E22CE - Highlights / Badges
COLOR_LIGHT_PURPLE = RGBColor(243, 232, 255)   # #F3E8FF - Card Background Tints
COLOR_BORDER_PURPLE = RGBColor(216, 180, 254)  # #D8B4FE - Card Outlines
COLOR_BODY_TEXT = RGBColor(30, 27, 75)         # #1E1B4B - High Contrast Dark Purple-Navy
COLOR_MUTED_TEXT = RGBColor(107, 114, 128)     # #6B7280 - Metadata / Footers

FONT_FAMILY = "Calibri"

# Target font sizes specified by user
FONT_SIZE_TITLE = Pt(35)
FONT_SIZE_SUBTITLE = Pt(25)
FONT_SIZE_BODY = Pt(20)


# -----------------------------------------------------------------------------
# Image Generator Helpers
# -----------------------------------------------------------------------------
def ensure_images_directory(img_dir: str):
    """Ensures target directory exists."""
    os.makedirs(img_dir, exist_ok=True)


def create_pipeline_diagram(output_path: str):
    """Creates a high-resolution 4-stage pipeline architectural diagram."""
    fig, ax = plt.subplots(figsize=(8, 3.8), dpi=250)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")

    stages = [
        ("1. Data Ingestion", "Streamlit UI\n• Student Details\n• 5 Subject Scores\n• Attendance %", "#3B0764"),
        ("2. Rule Processor", "data_processor.py\n• Boundary Check\n• Aggregates & %\n• Category & Advice", "#581C87"),
        ("3. Visualization", "visualizer.py\n• Matplotlib Agg\n• Comparative Bars\n• Threshold Lines", "#7E22CE"),
        ("4. PDF Engine", "pdf_generator.py\n• Platypus Layout\n• Embedded Chart\n• In-Memory PDF", "#3B0764"),
    ]

    for i, (title, desc, color) in enumerate(stages):
        x = i * 2.1
        # Card box
        rect = patches.FancyBboxPatch(
            (x, 0.2), 1.8, 2.8,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            edgecolor=color, facecolor="#F5F3FF", linewidth=2.0
        )
        ax.add_patch(rect)
        # Header banner
        header_rect = patches.FancyBboxPatch(
            (x, 2.3), 1.8, 0.7,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            edgecolor=color, facecolor=color, linewidth=1.5
        )
        ax.add_patch(header_rect)
        ax.text(x + 0.9, 2.65, title, ha="center", va="center", color="#FFFFFF", fontsize=9.5, fontweight="bold")
        ax.text(x + 0.9, 1.25, desc, ha="center", va="center", color="#1E1B4B", fontsize=8.5, linespacing=1.4)

        # Arrow to next stage
        if i < 3:
            ax.annotate(
                "", xy=(x + 2.05, 1.6), xytext=(x + 1.85, 1.6),
                arrowprops=dict(arrowstyle="->", color="#7E22CE", lw=3.0, mutation_scale=16)
            )

    ax.set_xlim(-0.2, 8.4)
    ax.set_ylim(0.0, 3.3)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=250)
    plt.close(fig)


def create_performance_chart(output_path: str):
    """Creates a sample comparative academic bar chart."""
    subjects = ["Adv Python", "DSA", "DBMS", "ML Found.", "Web Tech"]
    scores = [95, 89, 92, 96, 88]
    colors = ["#3B0764", "#581C87", "#7E22CE", "#3B0764", "#581C87"]

    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=250)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFAFA")

    bars = ax.bar(subjects, scores, color=colors, width=0.55, edgecolor="#1E1B4B", linewidth=1.0, zorder=3)

    # Reference lines
    ax.axhline(50, color="#DC2626", linestyle=":", linewidth=1.5, alpha=0.8, label="Pass Benchmark (50)", zorder=2)
    avg_score = sum(scores) / len(scores)
    ax.axhline(avg_score, color="#7E22CE", linestyle="--", linewidth=1.8, alpha=0.9, label=f"Aggregate ({avg_score:.1f}%)", zorder=2)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h}", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E1B4B")

    ax.set_ylim(0, 115)
    ax.set_ylabel("Marks Obtained (/100)", fontsize=10, fontweight="bold", color="#3B0764")
    ax.set_title("Student Subject-Wise Performance Breakdown", fontsize=12, fontweight="bold", pad=12, color="#3B0764")
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color="#C4B5FD", zorder=1)
    ax.xaxis.grid(False)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#581C87")
    ax.spines["bottom"].set_color("#581C87")

    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#DDD6FE", fontsize=8.5)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=250)
    plt.close(fig)


def create_threshold_diagram(output_path: str):
    """Creates an academic threshold scale graphic."""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=250)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")

    tiers = [
        ("Excellent", ">= 85%", "Outstanding Subject Mastery & Honors", "#3B0764"),
        ("Good", "70% - 84.9%", "Strong Foundational Competence", "#581C87"),
        ("Average", "50% - 69.9%", "Meets Standard Passing Benchmark", "#7E22CE"),
        ("Needs Improvement", "< 50%", "Remedial Counseling Required", "#9333EA")
    ]

    for idx, (title, rng, desc, color) in enumerate(tiers):
        y = 2.8 - (idx * 0.85)
        # Category Badge
        b_rect = patches.FancyBboxPatch((0.2, y), 2.2, 0.65, boxstyle="round,pad=0.08,rounding_size=0.1",
                                        facecolor=color, edgecolor=color)
        ax.add_patch(b_rect)
        ax.text(1.3, y + 0.325, f"{title}\n({rng})", ha="center", va="center", color="#FFFFFF",
                fontsize=9.5, fontweight="bold")

        # Description Card
        c_rect = patches.FancyBboxPatch((2.6, y), 4.7, 0.65, boxstyle="round,pad=0.08,rounding_size=0.1",
                                        facecolor="#F5F3FF", edgecolor="#DDD6FE", linewidth=1.5)
        ax.add_patch(c_rect)
        ax.text(2.8, y + 0.325, desc, ha="left", va="center", color="#1E1B4B", fontsize=9.5, fontweight="bold")

    ax.set_xlim(0, 7.6)
    ax.set_ylim(0, 3.6)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=250)
    plt.close(fig)


def create_pdf_mockup_graphic(output_path: str):
    """Creates a visual preview schematic of the ReportLab PDF structure."""
    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=250)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")

    # Outer Sheet (A4 Representation)
    sheet = patches.FancyBboxPatch((0.5, 0.2), 6.5, 3.6, boxstyle="round,pad=0.08,rounding_size=0.1",
                                   facecolor="#FAFAFA", edgecolor="#581C87", linewidth=2.0)
    ax.add_patch(sheet)

    # Header Box
    hdr = patches.Rectangle((0.8, 3.1), 5.9, 0.5, facecolor="#3B0764", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(3.75, 3.35, "INSTITUTE OF ADVANCED STUDIES & RESEARCH\nOFFICIAL PERFORMANCE TRANSCRIPT",
            ha="center", va="center", color="#FFFFFF", fontsize=7.5, fontweight="bold")

    # Student Profile Bar
    prof = patches.Rectangle((0.8, 2.5), 5.9, 0.45, facecolor="#EDE9FE", edgecolor="#C4B5FD", linewidth=1.0)
    ax.add_patch(prof)
    ax.text(3.75, 2.72, "Student: Aarav Sharma  |  Roll: 24CS801  |  Dept: CSE  |  Attendance: 94.5% (Satisfactory)",
            ha="center", va="center", color="#1E1B4B", fontsize=7.0, fontweight="bold")

    # Coursework Table Block
    tbl = patches.Rectangle((0.8, 1.55), 5.9, 0.8, facecolor="#FFFFFF", edgecolor="#C4B5FD", linewidth=1.0)
    ax.add_patch(tbl)
    ax.text(3.75, 1.95, "[ Coursework Marks Table: Max Marks, Obtained, Letter Grade, Pass Status ]\nGrand Total: 457 / 500  |  Aggregate: 91.4% (EXCELLENT)",
            ha="center", va="center", color="#3B0764", fontsize=7.0, fontweight="bold")

    # Embedded Chart & Feedback Blocks
    cht = patches.Rectangle((0.8, 0.75), 2.8, 0.65, facecolor="#F3E8FF", edgecolor="#DDD6FE", linewidth=1.0)
    ax.add_patch(cht)
    ax.text(2.2, 1.07, "Embedded Matplotlib\nComparative Chart", ha="center", va="center", color="#581C87", fontsize=6.8, fontweight="bold")

    fb = patches.Rectangle((3.8, 0.75), 2.9, 0.65, facecolor="#F5F3FF", edgecolor="#DDD6FE", linewidth=1.0)
    ax.add_patch(fb)
    ax.text(5.25, 1.07, "Personalized Feedback Box\nStrengths & Growth Areas", ha="center", va="center", color="#581C87", fontsize=6.8, fontweight="bold")

    # Signatures
    ax.text(3.75, 0.42, "Class Advisor Line   -------------------   Head of Department   -------------------   Dean Academics",
            ha="center", va="center", color="#6B7280", fontsize=6.0)

    ax.set_xlim(0, 7.5)
    ax.set_ylim(0, 4.0)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=250)
    plt.close(fig)


# -----------------------------------------------------------------------------
# PPTX Builder Utilities
# -----------------------------------------------------------------------------
def set_slide_background_white(slide):
    """Sets a clean pure white background for the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_WHITE


def add_dark_purple_accents(slide):
    """Adds subtle modern dark purple accent lines/borders to the slide."""
    # Top accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.04))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = COLOR_DEEP_PURPLE
    top_line.line.color.rgb = COLOR_DEEP_PURPLE

    # Bottom footer banner
    footer_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.02))
    footer_bar.fill.solid()
    footer_bar.fill.fore_color.rgb = COLOR_BORDER_PURPLE
    footer_bar.line.color.rgb = COLOR_BORDER_PURPLE


def add_slide_header(slide, title_text: str, subtitle_text: str):
    """
    Standardized header with EXACT requested font sizes:
    - Title: 35 pt
    - Subtitle: 25 pt
    """
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Title paragraph (35 pt)
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_FAMILY
    p_title.font.size = FONT_SIZE_TITLE
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_DARK_PURPLE

    # Subtitle paragraph (25 pt)
    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = FONT_SIZE_SUBTITLE
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_DEEP_PURPLE


def add_bullet_content(slide, left: float, top: float, width: float, height: float, bullet_items: list):
    """
    Adds bulleted body text with EXACT requested font size:
    - Text: 20 pt
    """
    textbox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = textbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    for i, item in enumerate(bullet_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        p.space_before = Pt(4)

        if isinstance(item, tuple):
            # (Bold header, normal text)
            run_bold = p.add_run()
            run_bold.text = item[0] + " "
            run_bold.font.name = FONT_FAMILY
            run_bold.font.size = FONT_SIZE_BODY
            run_bold.font.bold = True
            run_bold.font.color.rgb = COLOR_DARK_PURPLE

            run_body = p.add_run()
            run_body.text = item[1]
            run_body.font.name = FONT_FAMILY
            run_body.font.size = FONT_SIZE_BODY
            run_body.font.bold = False
            run_body.font.color.rgb = COLOR_BODY_TEXT
        else:
            run = p.add_run()
            run.text = item
            run.font.name = FONT_FAMILY
            run.font.size = FONT_SIZE_BODY
            run.font.bold = False
            run.font.color.rgb = COLOR_BODY_TEXT


def add_slide_footer(slide, current_slide: int, total_slides: int = 10):
    """Adds slide number and course information to footer."""
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"Advanced Python Programming  |  Personalized Report Generation  |  Slide {current_slide} of {total_slides}"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED_TEXT


# -----------------------------------------------------------------------------
# Main PPTX Builder
# -----------------------------------------------------------------------------
def build_presentation(output_pptx_path: str, images_dir: str):
    """Compiles the complete 10-slide PowerPoint deck."""
    print("Initializing PowerPoint presentation...")
    prs = Presentation()
    # 16:9 Widescreen format (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Generate supporting image assets
    print("Generating presentation graphics...")
    ensure_images_directory(images_dir)
    img_pipeline = os.path.join(images_dir, "pipeline_architecture.png")
    img_chart = os.path.join(images_dir, "performance_chart.png")
    img_threshold = os.path.join(images_dir, "threshold_scale.png")
    img_pdf = os.path.join(images_dir, "pdf_mockup.png")

    create_pipeline_diagram(img_pipeline)
    create_performance_chart(img_chart)
    create_threshold_diagram(img_threshold)
    create_pdf_mockup_graphic(img_pdf)

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    print("Building Slide 1: Title Slide...")
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s1)

    # Decorative purple header banner
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_DARK_PURPLE
    banner.line.color.rgb = COLOR_DARK_PURPLE

    # Main Title (35 pt)
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.4))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Personalized Report Generation using Templates and Python"
    p1.font.name = FONT_FAMILY
    p1.font.size = FONT_SIZE_TITLE
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK_PURPLE

    # Subtitle (25 pt)
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Automated Academic Performance Appraisal & PDF Compilation System"
    p1_sub.font.name = FONT_FAMILY
    p1_sub.font.size = FONT_SIZE_SUBTITLE
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = COLOR_DEEP_PURPLE
    p1_sub.space_before = Pt(8)

    # Project Details Card
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(11.7), Inches(3.3))
    card1.fill.solid()
    card1.fill.fore_color.rgb = COLOR_LIGHT_PURPLE
    card1.line.color.rgb = COLOR_BORDER_PURPLE
    card1.line.width = Pt(1.5)

    bullets_s1 = [
        ("• Academic Context:", "Postgraduate Seminar Coursework in Advanced Python Programming."),
        ("• Core Technology:", "Python 3, Streamlit (Web UI), Pandas (Data), Matplotlib (Charts), ReportLab (PDFs)."),
        ("• Key Philosophy:", "100% Free & Open-Source Stack — Zero external APIs, databases, or cloud costs."),
        ("• Architecture:", "Template Decoupled Design with In-Memory Byte Buffer Streaming (io.BytesIO).")
    ]
    add_bullet_content(s1, 1.2, 3.4, 10.9, 2.9, bullets_s1)
    add_slide_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    print("Building Slide 2: Problem Statement...")
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s2)
    add_slide_header(s2, "Problem Statement & Academic Motivation", "Challenges in Traditional Student Progress Reporting")
    add_dark_purple_accents(s2)

    bullets_s2 = [
        ("• High Administrative Overhead:", "Manual report preparation across spreadsheets is slow and labor-intensive."),
        ("• Arithmetic Calculation Errors:", "Manual averaging and grading often produce discrepancies in student grade cards."),
        ("• Lack of Personalized Guidance:", "Standard reports only show scores, lacking individualized academic advice."),
        ("• Absent Data Visualizations:", "Tabular marks alone fail to visually communicate strengths and growth areas."),
        ("• Need for Consistent Templating:", "Institutions require unified, professional branding across all student transcripts.")
    ]
    add_bullet_content(s2, 0.8, 1.8, 11.7, 5.0, bullets_s2)
    add_slide_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: Proposed Solution & Key Objectives
    # =========================================================================
    print("Building Slide 3: Proposed Solution...")
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s3)
    add_slide_header(s3, "Proposed Solution & System Objectives", "Automated, Decoupled Template-Driven Pipeline")
    add_dark_purple_accents(s3)

    bullets_s3 = [
        ("• Strict Input Validation:", "Real-time boundary checks (0–100 limits, required registration fields)."),
        ("• Automated Statistical Engine:", "Instant computation of totals, averages, percentages, and standing categories."),
        ("• Rule-Based Appraisal Engine:", "Generates intelligent feedback identifying top subjects and attendance warnings."),
        ("• Publication-Ready Visuals:", "Dynamic comparative bar charts highlighting benchmarks and student averages."),
        ("• Vector PDF Generation:", "ReportLab Platypus compiles print-ready academic documents on demand.")
    ]
    add_bullet_content(s3, 0.8, 1.8, 11.7, 5.0, bullets_s3)
    add_slide_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: System Architecture & Pipeline (With Architecture Diagram)
    # =========================================================================
    print("Building Slide 4: System Architecture...")
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s4)
    add_slide_header(s4, "System Architecture & Processing Pipeline", "4-Stage Modular Decoupled Design")
    add_dark_purple_accents(s4)

    # Left: Bullet text
    bullets_s4 = [
        ("• Stage 1 (Ingestion):", "Streamlit UI captures student demographics & 5 subject marks."),
        ("• Stage 2 (Processing):", "data_processor.py executes validation & statistical aggregations."),
        ("• Stage 3 (Analytics):", "visualizer.py produces comparative charts via Matplotlib Agg."),
        ("• Stage 4 (Compilation):", "pdf_generator.py binds data into ReportLab Platypus PDF.")
    ]
    add_bullet_content(s4, 0.8, 1.75, 5.8, 5.0, bullets_s4)

    # Right: Embedded Architecture Diagram
    if os.path.exists(img_pipeline):
        s4.shapes.add_picture(img_pipeline, Inches(6.8), Inches(1.85), width=Inches(5.7))

    add_slide_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: Technology Stack & Technical Rationale
    # =========================================================================
    print("Building Slide 5: Technology Stack...")
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s5)
    add_slide_header(s5, "Technology Stack & Technical Rationale", "100% Free, Lightweight & Open-Source Stack")
    add_dark_purple_accents(s5)

    bullets_s5 = [
        ("• Python 3:", "Core logic, strict type hinting, and memory-efficient byte streaming (io.BytesIO)."),
        ("• Streamlit:", "Reactive web interface with persistent session state management and custom CSS."),
        ("• Pandas:", "Tabular data frame structures for structured academic record manipulation."),
        ("• Matplotlib (Agg):", "Headless, thread-safe charting that prevents GUI backend threading crashes."),
        ("• ReportLab Platypus:", "Native vector PDF compilation with tables and flowables (no external OS tools).")
    ]
    add_bullet_content(s5, 0.8, 1.8, 11.7, 5.0, bullets_s5)
    add_slide_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: Input Validation & Categorization (With Threshold Diagram)
    # =========================================================================
    print("Building Slide 6: Validation & Categorization...")
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s6)
    add_slide_header(s6, "Input Validation & Academic Categorization", "Clearly Defined Academic Thresholds & Constraints")
    add_dark_purple_accents(s6)

    bullets_s6 = [
        ("• Boundary Enforcement:", "Name & Roll required; marks & attendance strictly in [0, 100]."),
        ("• Four Academic Tiers:", "Excellent (>= 85%), Good (70-84%), Average (50-69%), Needs Imprv (< 50%)."),
        ("• Attendance Compliance:", "Standard >= 75% required; < 75% triggers an immediate Shortage Alert."),
        ("• Multi-Factor Feedback:", "Praises highest subject while highlighting targeted areas for growth.")
    ]
    add_bullet_content(s6, 0.8, 1.75, 5.8, 5.0, bullets_s6)

    # Right: Embedded Threshold Diagram
    if os.path.exists(img_threshold):
        s6.shapes.add_picture(img_threshold, Inches(6.8), Inches(1.85), width=Inches(5.7))

    add_slide_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: Dynamic Data Visualization (With Performance Chart Image)
    # =========================================================================
    print("Building Slide 7: Visualization Engine...")
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s7)
    add_slide_header(s7, "Dynamic Data Visualization Engine", "In-Memory Academic Performance Analytics")
    add_dark_purple_accents(s7)

    bullets_s7 = [
        ("• Dynamic Bar Palette:", "Scores color-coded based on performance tiers for instant clarity."),
        ("• Benchmark Reference Lines:", "Passing mark threshold (50) and dynamic student average line."),
        ("• Value Annotations:", "Numerical scores explicitly annotated above each bar for readability."),
        ("• Zero-Disk Byte Buffering:", "Chart rasterized directly to io.BytesIO for web & PDF embedding.")
    ]
    add_bullet_content(s7, 0.8, 1.75, 5.8, 5.0, bullets_s7)

    # Right: Embedded Matplotlib Chart
    if os.path.exists(img_chart):
        s7.shapes.add_picture(img_chart, Inches(6.8), Inches(1.85), width=Inches(5.7))

    add_slide_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: Template Decoupling & PDF Generation (With PDF Mockup)
    # =========================================================================
    print("Building Slide 8: Template Decoupling & PDF...")
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s8)
    add_slide_header(s8, "Template Decoupling & Vector PDF Output", "Reusable Document Layout via ReportLab Platypus")
    add_dark_purple_accents(s8)

    bullets_s8 = [
        ("• Decoupled Architecture:", "Layout geometry remains static while dynamic student data is injected."),
        ("• Platypus Flowables:", "Uses Paragraphs, Tables, and KeepTogether to prevent page overflows."),
        ("• Institutional Elements:", "Header branding, grade tables, embedded charts, and signature blocks."),
        ("• Scalable Output:", "Clean vector PDF ready for immediate printing or official distribution.")
    ]
    add_bullet_content(s8, 0.8, 1.75, 5.8, 5.0, bullets_s8)

    # Right: Embedded PDF Structure Mockup
    if os.path.exists(img_pdf):
        s8.shapes.add_picture(img_pdf, Inches(6.8), Inches(1.85), width=Inches(5.7))

    add_slide_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: Demonstration & User Interface
    # =========================================================================
    print("Building Slide 9: Demonstration & Workflow...")
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s9)
    add_slide_header(s9, "Application Interface & Demonstration Workflow", "Streamlit Interactive Dashboard Experience")
    add_dark_purple_accents(s9)

    bullets_s9 = [
        ("• Quick Demo Presets:", "Sidebar allows 1-click loading of student profiles (High Achiever, Needs Review)."),
        ("• Dual-Tab Interface:", "Tab 1 for intuitive record entry; Tab 2 for live report inspection & download."),
        ("• Real-Time KPI Cards:", "Displays Total Marks, Aggregate %, Standing Badge, and Attendance."),
        ("• One-Click PDF Download:", "Streamlit download button serves vector-quality report on demand.")
    ]
    add_bullet_content(s9, 0.8, 1.8, 11.7, 5.0, bullets_s9)
    add_slide_footer(s9, 9)

    # =========================================================================
    # SLIDE 10: Conclusion, Future Scope & Q&A
    # =========================================================================
    print("Building Slide 10: Conclusion & Future Scope...")
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background_white(s10)
    add_slide_header(s10, "Conclusion, Future Scope & Viva Discussion", "Project Summary & Advanced Scalability Roadmap")
    add_dark_purple_accents(s10)

    bullets_s10 = [
        ("• Key Accomplishments:", "Delivered an automated, zero-cost, template-driven report generator."),
        ("• High Memory Efficiency:", "In-memory streaming (io.BytesIO) prevents disk clutter and file locking."),
        ("• Scalability Roadmap:", "Can easily extend to batch CSV processing for 500+ students and email dispatch."),
        ("• Advanced Extensions:", "Longitudinal trend tracking across semesters & institutional LMS integration."),
        ("• Thank You:", "Floor is open for Questions, Code Walkthrough, and Viva Evaluation.")
    ]
    add_bullet_content(s10, 0.8, 1.8, 11.7, 5.0, bullets_s10)
    add_slide_footer(s10, 10)

    # Save presentation
    prs.save(output_pptx_path)
    print(f"Presentation successfully generated and saved to: {output_pptx_path}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "personalized_report_presentation.pptx")
    img_folder = os.path.join(current_dir, "images")
    build_presentation(output_file, img_folder)
