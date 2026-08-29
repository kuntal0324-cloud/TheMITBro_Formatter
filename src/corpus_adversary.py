from __future__ import annotations
import hashlib,re,random

CONFUSIONS={"0":"O","1":"l","5":"S","8":"B","−":"-","×":"x","Ω":"ohm"}

def deterministic_noise(text:str,seed:str,rate:float=.035)->str:
    """Inject reproducible OCR-like corruption without destroying every keyword."""
    rng=random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:16],16))
    chars=list(text)
    candidates=[i for i,c in enumerate(chars) if c in CONFUSIONS]
    for i in candidates:
        if rng.random()<rate:chars[i]=CONFUSIONS[chars[i]]
    noisy="".join(chars)
    # whitespace/layout noise
    noisy=re.sub(r" {2,}"," ",noisy)
    if rng.random()<.7:noisy=noisy.replace(" = ","= ")
    return noisy

def hostile_variants(case):
    variants=[("clean",case.text)]
    variants.append(("ocr_noise",deterministic_noise(case.text,case.case_id,.08)))
    variants.append(("layout_noise",re.sub(r"\n+", "  \n", case.text)))
    return tuple(variants)
