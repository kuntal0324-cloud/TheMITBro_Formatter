from src.question_paper_ir import PaperSpec,QuestionSpec
from src.question_paper_renderer import QuestionPaperRenderer

def test_identity_in_footer():
    p=PaperSpec(title='X',questions=[QuestionSpec('Q1','Text')],metadata={'paper_id':'TMB-X-123','paper_version':'1.0.0'})
    svg=QuestionPaperRenderer().render(p).pages[0].svg
    assert 'TMB-X-123' in svg and 'v1.0.0' in svg and 'Page 1 of 1' in svg
