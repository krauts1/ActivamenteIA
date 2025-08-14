from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.deps import get_rag_service, get_sql_service
from openai import OpenAI
import os


class QueryIn(BaseModel):
    question: str
    top_k: int = 6
    structured: bool = False


router = APIRouter(prefix="/query", tags=["query"])


@router.post("")
async def query(
        payload: QueryIn,
        rag=Depends(get_rag_service),
        sql=Depends(get_sql_service)):
    hits = rag.retrieve(payload.question, k=payload.top_k)
    sql_preview = None
    df = None
    if payload.structured:
        df = sql.preview()
        sql_preview = (
            df.head(10).to_markdown(index=False) if not df.empty else None
        )
    prompt = rag.build_prompt(payload.question, hits, sql_preview)
    api_key = os.getenv("LLM_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        answer = resp.choices[0].message.content
    else:
        answer = "[LLM-DUMMY] Agrega LLM_API_KEY en .env para respuestas reales"
    return {
        "answer": answer,
        "sources": [h.dict() for h in hits],
        "sql": (
            df.to_dict(orient="records")
            if payload.structured and sql_preview
            else None
        ),
    }
