import json,pytest
from src.secure_io import safe_child,SecurityViolation
from src.question_integrity import seal,atomic_write_json
from src.integrity_audit import audit_production_bank
def test_path_escape_rejected(tmp_path):
 with pytest.raises(SecurityViolation):safe_child(tmp_path,"../escape.txt")
def test_corrupted_record_detected(tmp_path):
 recdir=tmp_path/"records";recdir.mkdir()
 d=seal({"id":"Q1","text":"ok"});atomic_write_json(recdir/"Q1.json",d)
 assert audit_production_bank(tmp_path).valid
 d["text"]="tampered";(recdir/"Q1.json").write_text(json.dumps(d))
 assert not audit_production_bank(tmp_path).valid
