from src.question_paper_ir import PaperSpec,QuestionSpec
from src.publication_identity import build_identity
from src.professional_pdf import render_professional_pdf
from src.answer_solution_pdf import render_answer_solution_pdf

def p():
    return PaperSpec(title='PDF',exam='GATE_EE',questions=[QuestionSpec('Q1','Find $2+2$.',number=1,marks=1,metadata={'answer':'4','solution':'2+2=4.'})])

def test_paper_and_solution_pdfs(tmp_path):
    a=render_professional_pdf(p(),tmp_path/'paper.pdf')
    b=render_answer_solution_pdf(p(),build_identity(p()),tmp_path/'sol.pdf')
    for x in (a,b):
        assert x.read_bytes().startswith(b'%PDF-') and x.stat().st_size>1000
