from pathlib import Path
from src.question_paper_ir import PaperSpec,QuestionSpec
from src.professional_publisher import publish_release
from src.deterministic_build import file_sha256

def test_release_zip_is_byte_deterministic(tmp_path):
    paper=PaperSpec(
        title="Deterministic M44",
        exam="GATE_EE",
        duration_minutes=10,
        total_marks=1,
        questions=[QuestionSpec(id="Q1",text="Find 1+1.",number=1,marks=1,metadata={"answer":"2","solution":"1+1=2"})],
    )
    a=publish_release(paper,tmp_path/"a",version="2.0.0",revision=1)
    # rebuild an equivalent fresh PaperSpec to avoid metadata mutation effects
    paper2=PaperSpec(
        title="Deterministic M44",
        exam="GATE_EE",
        duration_minutes=10,
        total_marks=1,
        questions=[QuestionSpec(id="Q1",text="Find 1+1.",number=1,marks=1,metadata={"answer":"2","solution":"1+1=2"})],
    )
    b=publish_release(paper2,tmp_path/"b",version="2.0.0",revision=1)
    assert a.paper_id==b.paper_id
    assert file_sha256(a.package_path)==file_sha256(b.package_path)
