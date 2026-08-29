from __future__ import annotations
from pathlib import Path
import hashlib
import json


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_release_manifest(identity, files):
    return {
        "contract": "M42",
        "paper": identity.to_dict(),
        "files": [
            {"name": Path(p).name, "sha256": sha256_file(p), "bytes": Path(p).stat().st_size}
            for p in sorted(map(Path, files), key=lambda x: x.name)
        ],
    }


def write_release_manifest(identity, files, path):
    p = Path(path)
    p.write_text(json.dumps(build_release_manifest(identity, files), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p
