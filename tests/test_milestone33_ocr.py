
from src.question_ocr import extract_text
def test_txt_supported(tmp_path):
    p=tmp_path/"a.txt"; p.write_text("x")
    assert extract_text(p).confidence>=0.9
