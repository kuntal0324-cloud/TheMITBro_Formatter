from src.question_paper_ir import PaperSpec,QuestionSpec
from src.publication_identity import build_identity

def paper():
    return PaperSpec(title='X',exam='GATE_EE',questions=[QuestionSpec('Q1','Find $2+2$.',marks=1)])

def test_identity_is_stable():
    a=build_identity(paper());b=build_identity(paper())
    assert a==b and a.paper_id.startswith('TMB-GATE-EE-')

def test_version_revision():
    x=build_identity(paper(),version='2.1.0',revision=3)
    assert x.version=='2.1.0' and x.revision==3
