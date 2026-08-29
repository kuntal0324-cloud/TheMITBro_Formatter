import json
from pathlib import Path
from zipfile import ZipFile
from src.question_paper_ir import PaperSpec,QuestionSpec
from src.professional_publisher import publish_release

def test_release_package_is_complete(tmp_path):
    p=PaperSpec(title='Release',exam='GATE_EE',duration_minutes=10,total_marks=1,instructions=['Answer all questions.'],questions=[QuestionSpec('Q1','Find 2+2.',number=1,marks=1,metadata={'answer':'4','solution':'2+2=4.'})])
    r=publish_release(p,tmp_path,version='1.2.0')
    names={x.split('/')[-1] for x in ZipFile(r.package_path).namelist()}
    assert {'paper.md','paper.html','paper.pdf','answers-solutions.md','answers-solutions.html','answers-solutions.pdf','paper-spec.json','manifest.json'}<=names
    m=json.loads((Path(r.release_dir)/'manifest.json').read_text())
    assert m['contract']=='M42' and len(m['files'])==7
