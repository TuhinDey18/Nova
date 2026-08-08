import faiss
import numpy as np
import pickle
import os


class FaissIndex:

    def __init__(self, dimension=512):

        self.dimension = dimension

        # Inner Product (Cosine Similarity after normalization)
        self.index = faiss.IndexFlatIP(dimension)

        self.metadata = []

    def add(self, embedding, info):

        embedding = np.asarray(
            embedding,
            dtype=np.float32
        ).reshape(1, -1)

        # Normalize for cosine similarity
        faiss.normalize_L2(embedding)

        self.index.add(embedding)

        self.metadata.append(info)

    def search(self, embedding, k=5):

        embedding = np.asarray(
            embedding,
            dtype=np.float32
        ).reshape(1, -1)

        # Normalize query
        faiss.normalize_L2(embedding)

        scores, indices = self.index.search(embedding, k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            results.append({
                "score": float(score),
                "info": self.metadata[idx]
            })

        return results

    def save(self, index_path):

        os.makedirs(os.path.dirname(index_path), exist_ok=True)

        faiss.write_index(
            self.index,
            index_path
        )

        metadata_path = os.path.join(
            os.path.dirname(index_path),
            "metadata.pkl"
        )

        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

        print(f"FAISS index saved: {index_path}")
        print(f"Metadata saved: {metadata_path}")

    def load(self, index_path):

        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"FAISS index not found: {index_path}"
            )

        self.index = faiss.read_index(index_path)

        metadata_path = os.path.join(
            os.path.dirname(index_path),
            "metadata.pkl"
        )

        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        print(f"Loaded {len(self.metadata)} embeddings.")