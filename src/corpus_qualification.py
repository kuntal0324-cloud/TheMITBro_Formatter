from __future__ import annotations
from collections import defaultdict
from .question_classifier import classify_question
from .question_intelligence import analyze_question
from .universal_math_recognizer import recognize_question_math
from .visual_question_analyzer import analyze_visual_question
from .corpus_qualification_schema import CaseResult,QualificationReport

def qualify_case(case,text=None):
    source=case.text if text is None else text
    c=classify_question(source,exam_hint=case.exam)
    qi=analyze_question(source,exam_hint=case.exam)
    math=recognize_question_math(source,ocr_confidence=.86 if "ocr_noise" in case.tags else 1.0)
    visual=analyze_visual_question(source)

    actual_topic = qi.topic if qi.topic!="Review Required" else c.topic
    topic_aliases = {
        "Network Theory": {"Network Theory", "Electric Circuits"},
        "Measurements": {"Measurements", "Electrical Measurements"},
    }
    accepted_topics = topic_aliases.get(case.expected_topic, {case.expected_topic})
    classification_ok = actual_topic in accepted_topics or c.topic in accepted_topics
    type_ok = case.expected_type=="UNSPECIFIED" or qi.question_type==case.expected_type
    review_actual = bool(qi.review_required or c.status=="REVIEW")
    review_ok = review_actual if case.expected_review else True

    # Math qualification is conservative: noisy text may reduce confidence, but
    # must not collapse to a zero-confidence recognizer result.
    math_ok = math.math_confidence > 0.0

    visual_expected = (
        any(t in case.tags for t in ("graph","phasor","ray","fbd"))
        or "diagram" in source.lower()
        or "shown" in source.lower()
    )
    visual_ok = (not visual_expected) or visual.diagram_present

    diagnostics=[]
    if not classification_ok:diagnostics.append(f"topic:{actual_topic}")
    if not type_ok:diagnostics.append(f"type:{qi.question_type}")
    if not review_ok:diagnostics.append("review_gate")
    if not math_ok:diagnostics.append("math_confidence")
    if not visual_ok:diagnostics.append("visual_detection")

    passed=classification_ok and type_ok and review_ok and math_ok and visual_ok
    return CaseResult(case.case_id,passed,classification_ok,type_ok,review_ok,math_ok,visual_ok,
                      case.expected_topic,actual_topic,tuple(diagnostics))

def qualify_corpus(cases):
    results=tuple(qualify_case(c) for c in cases)
    subjects=defaultdict(lambda:{"total":0,"passed":0})
    tags=defaultdict(lambda:{"total":0,"passed":0})
    for c,r in zip(cases,results):
        subjects[c.subject]["total"]+=1;subjects[c.subject]["passed"]+=int(r.passed)
        for tag in c.tags:
            tags[tag]["total"]+=1;tags[tag]["passed"]+=int(r.passed)
    for d in (subjects,tags):
        for v in d.values():
            v["pass_rate"]=round(v["passed"]/v["total"],4) if v["total"] else 0.0
    passed=sum(r.passed for r in results)
    return QualificationReport(len(results),passed,len(results)-passed,
        round(passed/len(results),4) if results else 0.0,
        dict(subjects),dict(tags),results)
