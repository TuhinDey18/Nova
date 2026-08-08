from embedding import EmbeddingExtractor
from faiss_index import FaissIndex


class SearchEngine:

    def __init__(self):

        self.embedder = EmbeddingExtractor()

        self.faiss = FaissIndex()

        self.faiss.load("faiss/faiss.index")

    def search_image(
        self,
        image_path,
        top_k=100
    ):

        embedding = self.embedder.extract(image_path)

        results = self.faiss.search(
            embedding,
            k=top_k
        )

        return results