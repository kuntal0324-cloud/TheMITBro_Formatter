from __future__ import annotations
from pathlib import Path
import random

def make_question_photo(text:str,path,*,seed=43,rotate_degrees=1.5,noise_points=450):
    """Create a reproducible photographed-page-like fixture using Pillow."""
    try:
        from PIL import Image,ImageDraw,ImageFont,ImageEnhance
    except ImportError as exc:
        raise RuntimeError("Photo fixture generation requires Pillow.") from exc
    rng=random.Random(seed)
    img=Image.new("L",(1200,900),245)
    draw=ImageDraw.Draw(img)
    font=ImageFont.load_default()
    y=70
    for raw in text.splitlines():
        draw.text((80,y),raw,fill=20,font=font)
        y+=28
    for _ in range(noise_points):
        x=rng.randrange(img.width);y=rng.randrange(img.height)
        shade=rng.choice((180,195,210,225))
        draw.point((x,y),fill=shade)
    img=img.rotate(rotate_degrees,expand=False,fillcolor=250)
    img=ImageEnhance.Contrast(img).enhance(.92)
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);img.save(p)
    return p
