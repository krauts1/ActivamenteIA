import numpy as np


class RandomEmbedder:
    def __init__(self, dim: int = 384):
        self.dim = dim

    def encode(self, text: str) -> np.ndarray:
        rng = np.random.default_rng(abs(hash(text)) % (2**32))
        V = rng.normal(size=(1, self.dim))
        V = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)
        return V.astype("float32")

    def encode_batch(self, texts):
        texts = list(texts)
        rng = np.random.default_rng(42)
        V = rng.normal(size=(len(texts), self.dim))
        V = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)
        return V.astype("float32")
