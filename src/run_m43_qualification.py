from __future__ import annotations
import json
from pathlib import Path
from .corpus_loader import load_builtin_corpus
from .corpus_qualification import qualify_corpus

def main(output="m43-qualification-report.json"):
    report=qualify_corpus(load_builtin_corpus())
    Path(output).write_text(json.dumps(report.to_dict(),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"M43 corpus: {report.passed}/{report.total} passed ({report.pass_rate:.1%})")
    return 0 if report.pass_rate>=.75 else 1

if __name__=="__main__":
    raise SystemExit(main())
