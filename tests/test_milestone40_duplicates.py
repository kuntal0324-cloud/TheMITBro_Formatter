from src.semantic_duplicate_detector import cosine_similarity,find_semantic_duplicate
def test_semantic_similarity():
 assert cosine_similarity("Find determinant of matrix A","Determine the determinant of matrix A")>.7
def test_near_duplicate():
 e=[{"id":"Q1","text":"Find determinant of matrix A"}]
 assert find_semantic_duplicate("Determine the determinant of matrix A",e).status in {"DUPLICATE","REVIEW"}
