from pathlib import Path
from PIL import Image
from src.image_preprocessor import preprocess

def test_preprocess_png(tmp_path: Path):
    source = tmp_path / "q.png"
    Image.new("RGB", (80, 40), "white").save(source)
    output = tmp_path / "clean.png"
    result = preprocess(source, output_path=output)
    assert output.exists()
    assert result.width == 80
    assert result.height == 40
    assert "grayscale" in result.operations
