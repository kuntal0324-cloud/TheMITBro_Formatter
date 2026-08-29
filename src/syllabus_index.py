from __future__ import annotations
from .question_taxonomy import NODES

def syllabus_tree(exam: str) -> dict:
    tree: dict = {}
    for n in NODES:
        if n.exam != exam:
            continue
        tree.setdefault(n.subject, {}).setdefault(n.topic, {}).setdefault(n.subtopic, []).append(n.concept)
    for subject in tree.values():
        for topic in subject.values():
            for subtopic, concepts in topic.items():
                topic[subtopic] = sorted(set(concepts))
    return tree

def syllabus_paths(exam: str) -> tuple[tuple[str,...], ...]:
    out=[]
    for n in NODES:
        if n.exam==exam:
            out.append((n.exam,n.subject,n.topic,n.subtopic,n.concept))
    return tuple(out)
