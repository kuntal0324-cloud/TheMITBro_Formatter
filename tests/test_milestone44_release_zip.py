from zipfile import ZipFile
from src.integrity_audit import audit_zip
def test_unsafe_zip_path_detected(tmp_path):
 p=tmp_path/"bad.zip"
 with ZipFile(p,"w") as z:z.writestr("../escape.txt","x")
 assert not audit_zip(p).valid
