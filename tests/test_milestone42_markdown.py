from src.question_paper_ir import PaperSpec,QuestionSpec
from src.publication_identity import build_identity
from src.professional_markdown import render_publication_markdown

def test_markdown_equation_matrix_table_preserved():
    q=QuestionSpec('Q1','''Let A =
[1  2]
[3  4]

| x | y |
|---|---|
| 1 | 2 |
''',number=1,marks=2,metadata={'answer':'B','solution':'Compute determinant = -2.'})
    p=PaperSpec(title='Math',exam='GATE_EE',questions=[q])
    x=render_publication_markdown(p,build_identity(p),include_answers=True,include_solutions=True)
    assert r'\begin{bmatrix}' in x
    assert '| x | y |' in x
    assert '## Answer Key' in x and '## Detailed Solutions' in x
