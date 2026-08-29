from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import stat

FIXED_ZIP_TIME=(2020,1,1,0,0,0)

def write_deterministic_zip(path,files,arc_root):
    p=Path(path);root=Path(arc_root)
    with ZipFile(p,"w",ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(map(Path,files),key=lambda x:x.name):
            info=ZipInfo(str(root/f.name).replace("\\","/"),date_time=FIXED_ZIP_TIME)
            info.compress_type=ZIP_DEFLATED
            info.create_system=3
            info.external_attr=(stat.S_IFREG | 0o644) << 16
            z.writestr(info,f.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
    return p
