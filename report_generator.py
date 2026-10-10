
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def make_report(
    filename,
    target_role,
    selected,
    found,
    found_required,
    missing,
    results,
    roadmap,
):
    """Generate a downloadable PDF report as bytes."""

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="AI Resume Analyzer Report",
        author="AI Resume Analyzer",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#17365D"),
            fontSize=19,
            leading=24,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            textColor=colors.HexColor("#17365D"),
            spaceBefore=12,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13,
        )
    )

    story = []

    def add_paragraph(value, style="BodyText"):
        story.append(Paragraph(str(value), styles[style]))

    def add_section(title):
        add_paragraph(escape(title), "SectionHeading")

    def add_bullets(items):
        if not items:
            add_paragraph("None detected.", "BodyText")
            return

        for item in items:
            add_paragraph(
                "&#8226; " + escape(str(item)),
                "BodyText",
            )

    add_paragraph(
        "AI RESUME ANALYZER",
        "ReportTitle",
    )
    add_paragraph(
        "Job Recommendation and Skill-Gap Analysis",
        "Heading2",
    )
    story.append(Spacer(1, 6))

    add_paragraph(
        f"<b>Generated:</b> "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    add_paragraph(
        f"<b>Resume file:</b> {escape(str(filename))}"
    )
    add_paragraph(
        f"<b>Target role:</b> {escape(str(target_role))}"
    )

    add_section("Match Summary")

    summary_data = [
        ["Metric", "Result"],
        [
            "Estimated match score",
            f"{float(selected['match_score']):.1f}%",
        ],
        [
            "Required-skill coverage",
            f"{float(selected['skill_coverage']):.1f}%",
        ],
        [
            "TF-IDF text similarity",
            f"{float(selected['text_similarity']):.1f}%",
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[95 * mm, 65 * mm],
        repeatRows=1,
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    story.append(summary_table)

    add_section("Detected Skills")
    add_bullets(found)

    add_section("Required Skills Detected")
    add_bullets(found_required)

    add_section("Required Skills Not Detected")
    add_bullets(missing)

    add_section("Top Three Job Recommendations")

    recommendation_data = [["Rank", "Job Role", "Match Estimate"]]

    for rank, (_, row) in enumerate(
        results.head(3).iterrows(),
        start=1,
    ):
        recommendation_data.append(
            [
                str(rank),
                escape(str(row["role"])),
                f"{float(row['match_score']):.1f}%",
            ]
        )

    recommendation_table = Table(
        recommendation_data,
        colWidths=[20 * mm, 95 * mm, 45 * mm],
        repeatRows=1,
    )

    recommendation_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    story.append(recommendation_table)

    add_section("Suggested Learning Roadmap")

    if roadmap:
        for item in roadmap:
            add_paragraph(
                f"<b>Priority {escape(str(item['Priority']))}: "
                f"{escape(str(item['Skill to learn']))}</b>"
            )
            add_paragraph(
                f"<b>Topic:</b> "
                f"{escape(str(item['Topic']))}"
            )
            add_paragraph(
                f"<b>Suggested activity:</b> "
                f"{escape(str(item['Suggested activity']))}"
            )
            story.append(Spacer(1, 4))
    else:
        add_paragraph(
            "No undetected required skills for this target role "
            "based on the current dictionary."
        )

    add_section("Limitations and Responsible Use")

    add_paragraph(
        "Match scores are project-defined estimates for educational "
        "guidance. They are not hiring probabilities or recruiter "
        "decisions."
    )
    add_paragraph(
        "A skill not detected in a resume is not proof that the "
        "candidate lacks that ability."
    )
    add_paragraph(
        "Results depend on extracted text, the controlled skill "
        "dictionary, and the curated job-role dataset."
    )

    def add_page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(
            A4[0] / 2,
            10 * mm,
            f"Page {document.page}",
        )
        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
