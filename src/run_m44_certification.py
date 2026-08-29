from __future__ import annotations
import sys
from .production_certification import write_certification
def main(path="m44-production-certification.json"):
    c=write_certification(path)
    print(f"M44 corpus qualification: {c.corpus_passed}/{c.corpus_total} ({c.corpus_pass_rate:.1%})")
    print("Ready for final certification:",c.ready_for_final_certification)
    return 0 if c.ready_for_final_certification else 1
if __name__=="__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv)>1 else "m44-production-certification.json"))
