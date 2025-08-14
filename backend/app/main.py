from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.health_router import router as health
from app.api.routers.ingest_router import router as ingest
from app.api.routers.query_router import router as query
from app.api.routers.sql_router import router as sql
from app.core.config import get_settings
from app.core.logging import setup_logging

logger = setup_logging()
settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health)
app.include_router(ingest)
app.include_router(query)
app.include_router(sql)
