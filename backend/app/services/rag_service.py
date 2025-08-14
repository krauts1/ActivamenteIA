from typing import Optional
from app.domain.models import SearchHit
from app.domain.ports import Embedder, VectorIndex, MetadataRepository


class RAGService:
    def __init__(
            self,
            embedder: Embedder,
            index: VectorIndex,
            meta_repo: MetadataRepository):
        self.embedder = embedder
        self.index = index
        self.meta_repo = meta_repo

    def retrieve(self, question: str, k: int = 6) -> list[SearchHit]:
        q_vec = self.embedder.encode(question)
        pairs = self.index.search(q_vec, k=k)
        hits: list[SearchHit] = []
        for rid, score in pairs:
            row = self.meta_repo.get_chunk_by_rid(rid)
            text, meta = (row if row else ("", {}))
            hits.append(SearchHit(rid=rid, score=score, text=text, meta=meta))
        return hits

    def build_prompt(
            self,
            question: str,
            hits: list[SearchHit],
            sql_preview: Optional[str] = None) -> str:
        ctx = "\n\n".join([f"(rid={h.rid}) {h.text}" for h in hits])
        sql_txt = (
            f"\n\n[SQL RESULT PREVIEW]\n{sql_preview}" if sql_preview else ""
        )
        return (
            (
                "Eres un asistente. Responde SOLO con la información del contexto.\n"
                "Si falta información, dilo y sugiere qué documento cargar.\n\n"
                f"Pregunta: {question}\n\nContexto:\n{ctx}{sql_txt}\n"
                "Devuelve una respuesta clara y cita los rids usados."
            )
        )
