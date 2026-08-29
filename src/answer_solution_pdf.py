from __future__ import annotations
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.units import mm
from xml.sax.saxutils import escape
from .publication_content import answer_entries


def render_answer_solution_pdf(paper, identity, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Answer Key", styles["Title"]),
        Paragraph(escape(identity.release_label), styles["Normal"]),
        Spacer(1, 6 * mm),
    ]
    for a in answer_entries(paper):
        story.append(Paragraph(f"<b>{a.number}.</b> {escape(a.answer)}", styles["BodyText"]))
    story += [
        PageBreak(),
        Paragraph("Detailed Solutions", styles["Title"]),
        Paragraph(escape(identity.release_label), styles["Normal"]),
        Spacer(1, 6 * mm),
    ]
    for a in answer_entries(paper):
        story.append(KeepTogether([
            Paragraph(f"Q{a.number}", styles["Heading2"]),
            Paragraph(escape(a.solution or "Detailed solution not supplied."), styles["BodyText"]),
            Spacer(1, 4 * mm),
        ]))
    doc = SimpleDocTemplate(
        str(p), pagesize=A4,
        rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=f"{paper.title} - Answers and Solutions",
        author="TheMITbro", invariant=1,
    )
    doc.build(story)
    return p
