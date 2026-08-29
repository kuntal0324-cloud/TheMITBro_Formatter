from __future__ import annotations
import json,re
from pathlib import Path
from .question_paper_ir import PaperSpec,QuestionSpec
from .answer_parser import parse_answer_bundle

def load_production_records(root)->list[dict]:
    base=Path(root)/"records"
    if not base.exists():return []
    out=[]
    for p in sorted(base.glob("*.json")):
        data=json.loads(p.read_text(encoding="utf-8"))
        data.pop("integrity_sha256",None)
        out.append(data)
    return out

def _options(text):
    return [m.group(2).strip() for m in re.finditer(r"(?m)^\s*([A-D])[\.\)]\s*(.+)$",text)]

def _stem(text):
    lines=[]
    for line in text.splitlines():
        if re.match(r"^\s*[A-D][\.\)]\s+",line):continue
        if re.match(r"^\s*\*\*(?:Answer|Correct Answer|Solution):\*\*",line,re.I):break
        lines.append(line)
    return "\n".join(lines).strip()

def to_paper_spec(generated)->PaperSpec:
    qs=[]
    for n,item in enumerate(generated.questions,1):
        bundle=parse_answer_bundle(item["text"])
        qs.append(QuestionSpec(
            id=item["id"],text=_stem(item["text"]),number=n,marks=item.get("marks"),
            options=_options(item["text"]),section=item.get("subject"),
            metadata={"topic":item.get("topic"),"concept":item.get("concept"),"M41":True,
                      "source_text":item["text"],"answer":bundle.answer,"solution":bundle.solution}
        ))
    duration=generated.blueprint.get("duration_minutes")
    total_marks=generated.blueprint.get("total_marks")
    return PaperSpec(
        title=generated.title,exam=generated.exam,duration_minutes=duration,
        total_marks=total_marks,questions=qs,
        instructions=["Generated deterministically from the M40 production Question Bank."],
        metadata={"generator_contract":"M41","metrics":generated.metrics}
    ).ensure_valid()
