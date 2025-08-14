from fastapi import APIRouter, Depends
from app.core.deps import get_index

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health(index=Depends(get_index)):
    return {"status": "ok", "index_size": index.ntotal}
