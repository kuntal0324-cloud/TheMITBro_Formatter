from __future__ import annotations
from dataclasses import dataclass,asdict
from .paper_blueprint import PaperBlueprint
from .mock_paper_generator import generate_mock_paper

@dataclass(frozen=True)
class MockPaperQualification:
    exam:str
    generated:bool
    question_count:int
    marks:int
    deterministic:bool
    error:str|None=None
    def to_dict(self):return asdict(self)

def qualify_mock_paper(bank,blueprint):
    try:
        a=generate_mock_paper(bank,blueprint)
        b=generate_mock_paper(bank,blueprint)
    except Exception as exc:
        return MockPaperQualification(blueprint.exam,False,0,0,False,str(exc))
    return MockPaperQualification(
        blueprint.exam,True,len(a.question_ids),a.metrics["total_marks"],
        a.question_ids==b.question_ids,None
    )
