from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import hashlib,json,tempfile
from .question_ingest import ingest
from .question_duplicate_detector import find_duplicate
from .question_quality_score import score_question
from .question_formatter import format_document

def _sha256(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def _md(q):
    lines=[f"### {q['id']}","",f"**Exam:** {q['exam']}",f"**Subject:** {q['subject']}",f"**Topic:** {q['topic']}",f"**Subtopic:** {q['subtopic']}",f"**Concept:** {q['concept']}",f"**Difficulty:** {q['difficulty']}",f"**Type:** {q['type']}",f"**Marks:** {q['marks']}","",q['stem'],""]
    for lab,opt in zip(('A','B','C','D'),q.get('options',[])): lines.append(f"{lab}. {opt}")
    if q.get('options'): lines.append("")
    a=q['answer']; a=','.join(a) if isinstance(a,list) else str(a)
    lines += [f"**Answer:** {a}","","**Solution:**",q['solution'],""]
    return '\n'.join(lines)
def qualify_batch(jsonl_path,handoff_path):
    jp,hp=Path(jsonl_path),Path(handoff_path); h=json.loads(hp.read_text())
    errs=[]
    if h.get('formatter_required_version')!='2.0.0': errs.append('Formatter version contract mismatch.')
    if _sha256(jp)!=h.get('source_sha256'): errs.append('Question Bank handoff checksum mismatch.')
    if errs:return {'status':'BLOCKED','errors':errs,'questions':[]}
    qs=[json.loads(x) for x in jp.read_text().splitlines() if x.strip()]; out=[]; prior=[]
    with tempfile.TemporaryDirectory(prefix='tmb-b001-') as td:
      td=Path(td)
      for q in qs:
        md=_md(q); p=td/f"{q['id']}.md"; p.write_text(md)
        rec=ingest(p,exam_hint='GATE_EE'); qual=score_question(rec); dup=find_duplicate(md,prior); rendered=format_document(md)
        ok=(rec.classification.exam=='GATE_EE' and rec.classification.subject=='Engineering Mathematics' and rec.classification.status in {'AUTO','REVIEW'} and dup.status=='ACCEPT' and bool(rendered.strip()))
        out.append({'question_id':q['id'],'source_revision':q['revision'],'classification':{'exam':rec.classification.exam,'subject':rec.classification.subject,'topic':rec.classification.topic,'status':rec.classification.status,'confidence':rec.classification.confidence},'question_intelligence':rec.metadata.get('question_intelligence',{}),'validation':{'status':rec.metadata.get('validation_status'),'answer_status':rec.metadata.get('answer_validation_status'),'solution_status':rec.metadata.get('solution_validation_status'),'review_required':rec.metadata.get('requires_validation_review'),'findings':rec.metadata.get('quality_findings',[])},'quality':qual.to_dict(),'duplicate':asdict(dup),'render':{'status':'PASS' if rendered.strip() else 'FAIL','bytes':len(rendered.encode())},'formatter_qualification':'PASS' if ok else 'REVIEW','independent_human_review':'PENDING','paper_eligible':False})
        prior.append({'id':q['id'],'text':md})
    passed=sum(x['formatter_qualification']=='PASS' for x in out)
    return {'qualification_contract':'GATE_EE_BATCH001_FORMATTER_V2_Q1','formatter_version':'2.0.0','source_sha256':_sha256(jp),'question_count':len(out),'formatter_pass_count':passed,'formatter_review_count':len(out)-passed,'paper_eligible_count':0,'independent_human_review_required':True,'release_gate':'BLOCKED','status':'PASS' if len(out)==h.get('question_count') else 'BLOCKED','questions':out}
def write_qualification(j,h,o):
    r=qualify_batch(j,h); Path(o).parent.mkdir(parents=True,exist_ok=True); Path(o).write_text(json.dumps(r,indent=2)); return r
