from src.production_bulk_import import import_production_directory
def test_production_bulk_import(tmp_path):
 src=tmp_path/"src";src.mkdir()
 (src/"a.txt").write_text("Find determinant det(A).",encoding="utf-8")
 (src/"b.txt").write_text("Find determinant det(A).",encoding="utf-8")
 out=tmp_path/"bank"
 s=import_production_directory(src,root=out,exam_hint="GATE EE")
 assert s.processed==2 and s.imported>=1 and s.duplicates>=1
 assert (out/"review_queue.json").exists()
