from pathlib import Path
def test_version_and_final_docs():
 assert Path("VERSION").read_text().strip()=="2.0.0"
 for p in [
  "docs/FINAL_V2_CERTIFICATION.md",
  "docs/milestones/M45/ACCEPTANCE.md",
  "docs/milestones/M45/RELEASE_NOTES.md",
  "content/README.md",
 ]:
  assert Path(p).is_file()
