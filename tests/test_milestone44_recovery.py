from src.recovery_manager import create_recovery_point,restore_recovery_point
def test_recovery_round_trip(tmp_path):
 p=tmp_path/"catalog.json";p.write_text("before")
 rp=create_recovery_point([p],tmp_path/"backup")
 p.write_text("after")
 assert restore_recovery_point(rp)
 assert p.read_text()=="before"
