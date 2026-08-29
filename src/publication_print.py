from __future__ import annotations
from copy import deepcopy
import re
from .question_paper_ir import PaperSpec


def readable_math_text(value: str) -> str:
    s = str(value)
    # Convert raw row blocks first, before the historical renderer normalizes them.
    lines = s.splitlines()
    out=[];i=0
    while i < len(lines):
        if lines[i].strip().startswith('[') and lines[i].strip().endswith(']'):
            rows=[]
            while i < len(lines) and lines[i].strip().startswith('[') and lines[i].strip().endswith(']'):
                rows.append(lines[i].strip()[1:-1].strip())
                i += 1
            out.append('[' + '; '.join(rows) + ']')
            continue
        out.append(lines[i]);i += 1
    s='\n'.join(out)
    s=s.replace('$$','').replace('$','')
    replacements={
        r'\Omega':'Ω',r'\omega':'ω',r'\pi':'π',r'\theta':'θ',r'\lambda':'λ',r'\mu':'μ',
        r'\sigma':'σ',r'\phi':'φ',r'\Delta':'Δ',r'\alpha':'α',r'\beta':'β',r'\gamma':'γ',
        r'\times':'×',r'\cdot':'·',r'\pm':'±',r'\le':'≤',r'\ge':'≥',r'\neq':'≠',r'\infty':'∞',
        r'\to':'→',r'\,':' ',
    }
    for a,b in replacements.items():s=s.replace(a,b)
    s=re.sub(r'\\mathrm\{([^{}]+)\}',r'\1',s)
    s=re.sub(r'\\operatorname\{([^{}]+)\}',r'\1',s)
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
    s=re.sub(r'\\sqrt\{([^{}]+)\}',r'√(\1)',s)
    s=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',s)
    s=re.sub(r'_\{([^{}]+)\}',r'_(\1)',s)
    return s


def prepare_print_paper(paper: PaperSpec) -> PaperSpec:
    p=deepcopy(paper)
    for q in p.questions:
        q.text=readable_math_text(q.text)
        q.options=[readable_math_text(x) for x in q.options]
        q.metadata=dict(q.metadata or {})
        q.metadata["m42_print_prepared"]=True
    return p
