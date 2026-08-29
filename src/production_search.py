from __future__ import annotations
from collections import defaultdict
import re

class ProductionIndex:
    def __init__(self):
        self.documents={}
        self.inverted=defaultdict(set)
    def add(self,item:dict):
        qid=item["id"];self.documents[qid]=item
        fields=[item.get("text",""),item.get("exam",""),item.get("subject",""),item.get("topic",""),
                item.get("subtopic",""),item.get("concept",""),item.get("question_type","")]
        for tok in set(re.findall(r"[a-z0-9]+"," ".join(map(str,fields)).lower())):
            self.inverted[tok].add(qid)
    def search(self,query="",**filters):
        ids=set(self.documents)
        toks=re.findall(r"[a-z0-9]+",query.lower())
        for t in toks:ids &= self.inverted.get(t,set())
        out=[]
        for qid in sorted(ids):
            x=self.documents[qid]
            if any(v is not None and x.get(k)!=v for k,v in filters.items()):continue
            out.append(x)
        return out
