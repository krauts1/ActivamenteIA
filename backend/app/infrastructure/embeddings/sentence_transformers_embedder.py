import numpy as np
from sentence_transformers import SentenceTransformer


class STEmbedder:
    def __init__(self, model_name: str, batch_size: int = 16):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.batch_size = batch_size

    def _normalize(self, arr: np.ndarray) -> np.ndarray:
        return arr / (np.linalg.norm(arr, axis=1, keepdims=True) + 1e-12)

    def encode(self, text: str) -> np.ndarray:
        v = self.model.encode(
            [text],
            batch_size=1,
            normalize_embeddings=False,
            convert_to_numpy=True)
        return self._normalize(v.astype("float32"))

    def encode_batch(self, texts):
        texts = list(texts)
        V = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=False,
            convert_to_numpy=True
        )
        V = self._normalize(V.astype("float32"))
        return V
