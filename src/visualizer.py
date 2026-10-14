"""
visualizer.py
=============
Generates professional academic charts using Matplotlib.
Supports both direct display in Streamlit and byte-buffer export
for ReportLab PDF embedding.
"""

import io
from typing import Dict, Tuple
import matplotlib
# Use the non-interactive Agg backend to avoid GUI threading conflicts in Streamlit
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_performance_chart(
    subjects: Dict[str, float],
    student_name: str = "",
    average_mark: float = None
) -> Tuple[plt.Figure, bytes]:
    """
    Creates an academic bar chart comparing marks across subjects.

    Args:
        subjects: Dictionary of subject names to marks (0-100).
        student_name: Optional student name for chart title.
        average_mark: Computed student average mark for reference line.

    Returns:
        (fig, img_bytes): The Matplotlib Figure object and its PNG image bytes.
    """
    subject_names = list(subjects.keys())
    marks = [float(subjects[k]) for k in subject_names]

    # Compute average if not passed
    if average_mark is None:
        average_mark = sum(marks) / len(marks) if marks else 0.0

    # Color palette based on score brackets
    bar_colors = []
    for mark in marks:
        if mark >= 85:
            bar_colors.append("#10B981")  # Emerald (Excellent)
        elif mark >= 70:
            bar_colors.append("#3B82F6")  # Blue (Good)
        elif mark >= 50:
            bar_colors.append("#F59E0B")  # Amber (Average)
        else:
            bar_colors.append("#EF4444")  # Red (Needs Review)

    # Abbreviate or wrap subject names if long for clean x-axis readability
    formatted_labels = []
    for name in subject_names:
        # Wrap long names cleanly over multiple lines
        words = name.split()
        if len(words) > 2:
            formatted_labels.append("\n".join([" ".join(words[:2]), " ".join(words[2:])]))
        else:
            formatted_labels.append(name)

    # Set up figure and axis with high DPI for crisp presentation
    fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=200)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFAFA")

    # Plot bars
    bars = ax.bar(
        formatted_labels,
        marks,
        color=bar_colors,
        width=0.55,
        edgecolor="#334155",
        linewidth=0.8,
        zorder=3
    )

    # Reference Line: Passing Mark (50)
    ax.axhline(
        y=50,
        color="#EF4444",
        linestyle=":",
        linewidth=1.2,
        alpha=0.75,
        label="Passing Mark (50)",
        zorder=2
    )

    # Reference Line: Student Average
    ax.axhline(
        y=average_mark,
        color="#4F46E5",
        linestyle="--",
        linewidth=1.5,
        alpha=0.85,
        label=f"Student Average ({average_mark:.1f})",
        zorder=2
    )

    # Add score text labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),  # 4 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#1E293B"
        )

    # Styling the axes
    ax.set_ylim(0, 115)
    ax.set_ylabel("Marks Obtained (Out of 100)", fontsize=10, fontweight="bold", color="#334155")
    
    title_text = f"Subject-wise Performance Breakdown"
    if student_name:
        title_text += f" — {student_name}"
    ax.set_title(title_text, fontsize=12, fontweight="bold", pad=14, color="#0F172A")

    # Grid styling
    ax.yaxis.grid(True, linestyle="--", alpha=0.35, color="#94A3B8", zorder=1)
    ax.xaxis.grid(False)

    # Remove top and right spines for a modern, clean aesthetic
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#94A3B8")
    ax.spines["bottom"].set_color("#94A3B8")

    # Ticks formatting
    ax.tick_params(axis="x", labelsize=9, colors="#1E293B")
    ax.tick_params(axis="y", labelsize=9, colors="#475569")

    # Legend positioning
    ax.legend(
        loc="upper right",
        frameon=True,
        facecolor="#FFFFFF",
        edgecolor="#E2E8F0",
        fontsize=8.5
    )

    plt.tight_layout()

    # Save to in-memory bytes buffer for PDF embedding
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    buf.seek(0)
    img_bytes = buf.getvalue()

    return fig, img_bytes
