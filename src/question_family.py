from __future__ import annotations
import hashlib,re

def _shape(text):
    x=text.lower()
    x=re.sub(r"[-+]?\d+(?:\.\d+)?","<n>",x)
    x=re.sub(r"\b(?:a|b|c|d)\.\s+.*","",x)
    x=re.sub(r"\s+"," ",x).strip()
    return x

def family_signature(record)->str:
    c=record.classification
    m=record.metadata
    concept=str(m.get("concept") or c.topic)
    qtype=str(m.get("question_type") or "UNSPECIFIED")
    shape=_shape(record.text)
    # Family identity captures taxonomy + task form while tolerating numeric variants.
    key="|".join((c.exam,c.subject,c.topic,concept,qtype,shape[:240]))
    return hashlib.sha256(key.encode()).hexdigest()[:20]

def family_id(record)->str:
    return "QF-"+family_signature(record).upper()
