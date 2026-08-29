from src.final_release_manifest import build_final_manifest
def test_final_manifest_declares_frozen_baseline():
 m=build_final_manifest(".")
 assert m["release"]=="v2.0.0"
 assert m["milestone"]=="M45"
 assert m["architecture_status"]=="FROZEN"
 assert m["content_production_status"]=="READY"
 assert len(m["contracts"]["milestones"])==44
