import faiss
import os
import numpy as np


class FaissIPIndex:
    def __init__(self, dim: int, path: str):
        self.path = path
        if os.path.exists(path):
            self.index = faiss.read_index(path)
        else:
            self.index = faiss.IndexFlatIP(dim)
        self.ntotal = self.index.ntotal

    def add(self, vectors: np.ndarray) -> list[int]:
        start = self.index.ntotal
        self.index.add(vectors)
        self.ntotal = self.index.ntotal
        return list(range(start, self.ntotal))

    def search(self, q_vec: np.ndarray, k: int = 6):
        distances, indices = self.index.search(q_vec, k)
        return [
            (int(idx), float(dist))
            for idx, dist in zip(indices[0], distances[0])
            if idx != -1
        ]

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        faiss.write_index(self.index, self.path)
