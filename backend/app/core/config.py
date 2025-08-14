from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ActivaMente RAG API"

    EMBEDDINGS_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDINGS_PROVIDER: str = "openai"
    EMBEDDINGS_OPENAI_MODEL: str = "text-embedding-3-small"
    EMBEDDINGS_BATCH_SIZE: int = 4

    MAX_PDF_PAGES: int = 20
    MAX_TOTAL_CHUNKS: int = 500

    INDEX_PATH: str = "/var/lib/rag/indexes/main.index"
    META_DB_PATH: str = "/var/lib/rag/indexes/meta.sqlite"
    DATA_DIR: str = "./data"

    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str | None = None

    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "rag-index-backups"
    S3_PREFIX: str = "dev/"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> "Settings":
    return Settings()
