from __future__ import annotations
from .pdf_production import render_paper_pdf
from .publication_print import prepare_print_paper


def render_professional_pdf(paper, output_path):
    return render_paper_pdf(prepare_print_paper(paper), output_path)
