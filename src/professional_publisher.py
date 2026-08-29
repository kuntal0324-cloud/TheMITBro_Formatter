from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import shutil
from .publication_identity import build_identity
from .professional_markdown import write_publication_markdown
from .professional_html import render_professional_html
from .professional_pdf import render_professional_pdf
from .answer_solution_pdf import render_answer_solution_pdf
from .publication_manifest import write_release_manifest
from .deterministic_zip import write_deterministic_zip

@dataclass(frozen=True)
class PublicationRelease:
    release_dir: str
    paper_id: str
    version: str
    files: tuple[str, ...]
    package_path: str
    contract: str = "M42"

    def to_dict(self):
        return asdict(self)


def publish_release(paper, output_dir, *, version="1.0.0", revision=1):
    paper.ensure_valid()
    identity = build_identity(paper, version=version, revision=revision)
    base = Path(output_dir) / identity.release_label
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)

    paper.metadata = dict(paper.metadata or {})
    paper.metadata.update({
        "paper_id": identity.paper_id,
        "paper_version": identity.version,
        "paper_revision": identity.revision,
        "publishing_contract": "M42",
    })

    md = write_publication_markdown(paper, identity, base / "paper.md", include_answers=False, include_solutions=False)
    html = render_professional_html(paper, identity, base / "paper.html", include_answers=False, include_solutions=False)
    pdf = render_professional_pdf(paper, base / "paper.pdf")
    fullmd = write_publication_markdown(paper, identity, base / "answers-solutions.md", include_answers=True, include_solutions=True)
    fullhtml = render_professional_html(paper, identity, base / "answers-solutions.html", include_answers=True, include_solutions=True)
    solpdf = render_answer_solution_pdf(paper, identity, base / "answers-solutions.pdf")
    spec = base / "paper-spec.json"
    spec.write_text(json.dumps(paper.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    files = [md, html, pdf, fullmd, fullhtml, solpdf, spec]
    manifest = write_release_manifest(identity, files, base / "manifest.json")
    files.append(manifest)

    package = Path(output_dir) / (identity.release_label + ".zip")
    write_deterministic_zip(package, files, Path(identity.release_label))

    return PublicationRelease(str(base), identity.paper_id, identity.version, tuple(str(x) for x in files), str(package))
