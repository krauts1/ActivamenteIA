from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.deps import get_sql_service


class SQLIn(BaseModel):
    sql: str
    limit: int = 200


router = APIRouter(prefix="/sql", tags=["sql"])


@router.post("/query")
async def sql_query(payload: SQLIn, svc=Depends(get_sql_service)):
    df = svc.run(payload.sql, limit=payload.limit)
    return {"rows": df.to_dict(orient="records")}
