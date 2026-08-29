from src.question_paper_ir import PaperSpec,QuestionSpec
from src.diagram_ir import DiagramSpec,Point,Axis
from src.publication_identity import build_identity
from src.professional_html import render_professional_html

def test_structured_diagram_published(tmp_path):
    d=DiagramSpec('coordinate_geometry',points=[Point(1,2,'A','A')],axes=[Axis('x'),Axis('y')])
    p=PaperSpec(title='Visual',questions=[QuestionSpec('Q1','Plot A(1,2).',number=1,diagrams=[d])])
    t=render_professional_html(p,build_identity(p),tmp_path/'v.html').read_text()
    assert '<svg' in t
