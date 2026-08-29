from src.photo_fixture_factory import make_question_photo
from src.image_preprocessor import preprocess
from PIL import Image
def test_photographed_question_fixture_preprocesses(tmp_path):
 p=make_question_photo("Find det(A) for A=[[1,2],[3,4]].",tmp_path/"photo.png")
 out=tmp_path/"processed.png"
 r=preprocess(p,output_path=out)
 assert out.exists() and r.width>0 and r.height>0
 with Image.open(out) as im: assert im.size==(r.width,r.height)
