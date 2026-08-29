from __future__ import annotations
from pathlib import Path
from .markdown_renderer import render_question
from .publication_content import answer_entries


def _question_markdown(q):
    lines = [f"### Q{q.number or q.id}" + (f" - {q.marks:g} mark(s)" if q.marks is not None else "")]
    if q.section:
        lines += [f"**Section:** {q.section}", ""]
    lines.append(render_question(q.text).strip())
    if q.options:
        lines.append("")
        for i, opt in enumerate(q.options):
            lines.append(f"{chr(65+i)}. {render_question(str(opt)).strip()}")
    if q.diagrams:
        lines += ["", f"> Diagram(s): {len(q.diagrams)} structured visual(s) attached in HTML/PDF publication."]
    return "\n".join(lines)


def render_publication_markdown(paper, identity, *, include_answers=False, include_solutions=False):
    paper.ensure_valid()
    meta = [
        f"# {paper.title}", "",
        f"**Paper ID:** `{identity.paper_id}`  ",
        f"**Version:** `{identity.version}` / Revision `{identity.revision}`  ",
    ]
    if paper.exam:
        meta.append(f"**Exam:** {paper.exam}  ")
    if paper.subject:
        meta.append(f"**Subject:** {paper.subject}  ")
    if paper.duration_minutes:
        meta.append(f"**Duration:** {paper.duration_minutes} minutes  ")
    meta += [f"**Total Marks:** {paper.resolved_total_marks():g}", ""]
    if paper.instructions:
        meta += ["## Instructions", ""] + [f"- {x}" for x in paper.instructions] + [""]
    body = ["## Questions", ""]
    for q in paper.questions:
        body += [_question_markdown(q), "", "---", ""]
    if include_answers:
        body += ["## Answer Key", ""]
        for a in answer_entries(paper):
            body.append(f"{a.number}. **{a.answer}**")
        body.append("")
    if include_solutions:
        body += ["## Detailed Solutions", ""]
        for a in answer_entries(paper):
            body += [f"### Q{a.number}", "", a.solution or "_Detailed solution not supplied._", ""]
    return "\n".join(meta + body).rstrip() + "\n"


def write_publication_markdown(paper, identity, path, **kwargs):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_publication_markdown(paper, identity, **kwargs), encoding="utf-8")
    return p
