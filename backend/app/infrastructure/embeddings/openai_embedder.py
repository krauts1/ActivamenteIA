from typing import Iterable, List
import numpy as np
import os
from openai import OpenAI


class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise RuntimeError("Falta LLM_API_KEY para OpenAI embeddings")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.dim = 1536

    def _norm(self, M: np.ndarray) -> np.ndarray:
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)

    def encode(self, text: str) -> np.ndarray:
        if not text:
            return np.zeros((1, self.dim), dtype="float32")
        r = self.client.embeddings.create(model=self.model, input=[text])
        v = np.array(r.data[0].embedding, dtype="float32").reshape(1, -1)
        return self._norm(v)

    def encode_batch(self, texts: Iterable[str]) -> np.ndarray:
        L = list(texts)
        if not L:
            return np.zeros((0, self.dim), dtype="float32")
        r = self.client.embeddings.create(model=self.model, input=L)
        arr: List[List[float]] = [d.embedding for d in r.data]
        V = np.array(arr, dtype="float32")
        return self._norm(V)
