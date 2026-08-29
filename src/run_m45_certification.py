from __future__ import annotations
import sys
from .final_certification import write_final_certification
from .final_release_manifest import write_final_manifest

def main(cert_path="m45-final-certification.json",manifest_path="M45_FINAL_BASELINE.json"):
    c=write_final_certification(cert_path)
    write_final_manifest(manifest_path)
    print(f"TheMITbro Formatter v{c.version}")
    print(f"Frozen historical contracts: {c.contracts_frozen}/44")
    print(f"Corpus qualification: {c.corpus_passed}/{c.corpus_total} ({c.corpus_pass_rate:.1%})")
    print("Architecture frozen:",c.architecture_frozen)
    print("Ready for real content:",c.ready_for_real_content)
    return 0 if c.ready_for_real_content else 1

if __name__=="__main__":
    raise SystemExit(main(*(sys.argv[1:3])))
