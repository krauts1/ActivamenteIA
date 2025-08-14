from pydantic import BaseModel
from typing import Any, Optional


class IngestResult(BaseModel):
    ok: bool
    file: str
    registered_in_sql: bool = False


class QueryRequest(BaseModel):
    question: str
    top_k: int = 6
    structured: bool = False


class SearchHit(BaseModel):
    rid: int
    score: float
    text: str
    meta: dict


class QueryResponse(BaseModel):
    answer: str
    sources: list[SearchHit]
    sql: Optional[list[dict[str, Any]]] = None
