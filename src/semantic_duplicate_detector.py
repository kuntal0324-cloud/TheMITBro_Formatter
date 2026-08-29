from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
import math,re
from .question_duplicate_detector import normalize_text,similarity

STOP={"the","a","an","of","to","is","are","in","for","and","or","with","given","find","determine","calculate","which"}

def tokens(text):
    return [x for x in re.findall(r"[a-z0-9]+",normalize_text(text)) if x not in STOP]

def cosine_similarity(a,b):
    ca,cb=Counter(tokens(a)),Counter(tokens(b))
    if not ca or not cb:return 0.0
    dot=sum(v*cb.get(k,0) for k,v in ca.items())
    na=math.sqrt(sum(v*v for v in ca.values()));nb=math.sqrt(sum(v*v for v in cb.values()))
    return round(dot/(na*nb),4) if na and nb else 0.0

@dataclass(frozen=True)
class SemanticDuplicate:
    status:str
    score:float
    lexical_score:float
    semantic_score:float
    matched_id:str|None=None

def find_semantic_duplicate(text,existing,*,duplicate_threshold=.92,review_threshold=.76):
    best=None
    for item in existing:
        other=str(item.get("text",""))
        if not other:continue
        lex=similarity(text,other);sem=cosine_similarity(text,other)
        # semantic bag-of-concepts and lexical sequence complement one another.
        score=round(.45*lex+.55*sem,4)
        cand=(score,lex,sem,item.get("id"))
        if best is None or cand[0]>best[0]:best=cand
    if best is None:return SemanticDuplicate("ACCEPT",0,0,0,None)
    score,lex,sem,mid=best
    if score>=duplicate_threshold:return SemanticDuplicate("DUPLICATE",score,lex,sem,mid)
    if score>=review_threshold:return SemanticDuplicate("REVIEW",score,lex,sem,mid)
    return SemanticDuplicate("ACCEPT",score,lex,sem,mid)
