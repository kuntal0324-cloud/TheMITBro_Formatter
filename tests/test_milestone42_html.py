from src.question_paper_ir import PaperSpec,QuestionSpec
from src.publication_identity import build_identity
from src.professional_html import render_professional_html

def test_self_contained_print_html(tmp_path):
    p=PaperSpec(title='HTML',exam='JEE',instructions=['Answer all.'],questions=[QuestionSpec('Q1','Find 2+2.',number=1,metadata={'answer':'4','solution':'2+2=4.'})])
    out=render_professional_html(p,build_identity(p),tmp_path/'x.html')
    t=out.read_text()
    assert '<svg ' in t and '@media print' in t and '<script src=' not in t
    assert 'themitbro-publication-manifest' in t
