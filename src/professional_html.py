from __future__ import annotations
from pathlib import Path
import html
import json
from .question_paper_ir import PaperSpec
from .question_paper_renderer import QuestionPaperRenderer
from .publication_content import answer_entries
from .publication_print import prepare_print_paper

CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; background:#eee; font-family:Arial,sans-serif; }
.paper-page { width:794px; min-height:1123px; margin:0 auto 24px; background:#fff; break-after:page; page-break-after:always; overflow:hidden; }
.answer-section, .solution-section { max-width:794px; margin:0 auto 24px; background:#fff; padding:48px 54px; }
.answer-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:8px 20px; }
.solution { break-inside:avoid; margin:0 0 22px; }
.release-meta { font-size:12px; color:#444; border-bottom:1px solid #bbb; padding-bottom:10px; margin-bottom:18px; }
@media print { html,body{background:#fff}.paper-page,.answer-section,.solution-section{margin:0;box-shadow:none} }
"""


def render_professional_html(paper, identity, path, *, include_answers=True, include_solutions=True):
    if not isinstance(paper, PaperSpec):
        paper = PaperSpec.from_dict(paper)
    result = QuestionPaperRenderer().render(prepare_print_paper(paper))
    pages = "\n".join(
        f'<section class="paper-page" data-page="{p.number}">{p.svg}</section>'
        for p in result.pages
    )
    entries = answer_entries(paper)
    answers = ""
    if include_answers:
        answers = (
            '<section class="answer-section"><h1>Answer Key</h1>'
            f'<div class="release-meta">{html.escape(identity.release_label)}</div>'
            '<div class="answer-grid">' +
            "".join(f'<div><b>{a.number}.</b> {html.escape(a.answer)}</div>' for a in entries) +
            '</div></section>'
        )
    solutions = ""
    if include_solutions:
        solutions = (
            '<section class="solution-section"><h1>Detailed Solutions</h1>'
            f'<div class="release-meta">{html.escape(identity.release_label)}</div>' +
            "".join(
                f'<article class="solution"><h2>Q{a.number}</h2><p>{html.escape(a.solution or "Detailed solution not supplied.")}</p></article>'
                for a in entries
            ) + '</section>'
        )
    manifest = {
        **result.manifest,
        "publication_contract": "M42",
        "paper_id": identity.paper_id,
        "version": identity.version,
        "revision": identity.revision,
        "content_sha256": identity.content_sha256,
    }
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(paper.title)}</title><style>{CSS}</style></head><body><main>{pages}{answers}{solutions}</main><script id="themitbro-publication-manifest" type="application/json">{json.dumps(manifest, sort_keys=True, separators=(",", ":"))}</script></body></html>'''
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")
    return p
