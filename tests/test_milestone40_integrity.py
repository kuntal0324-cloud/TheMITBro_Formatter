from src.question_integrity import seal,verify,atomic_write_json
import json
def test_seal_detects_corruption(tmp_path):
 d=seal({"id":"Q1","text":"abc"});assert verify(d)
 d["text"]="changed";assert not verify(d)
def test_atomic_write(tmp_path):
 p=tmp_path/"x.json";atomic_write_json(p,{"a":1});assert json.loads(p.read_text())=={"a":1}
