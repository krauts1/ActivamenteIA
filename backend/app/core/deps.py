from app.core.config import get_settings
from app.infrastructure.embeddings.sentence_transformers_embedder import (
    STEmbedder,
)
from app.infrastructure.embeddings.random_embedder import RandomEmbedder
from app.infrastructure.vector.faiss_index import FaissIPIndex
from app.infrastructure.repositories.sqlite_metadata_repo import (
    SQLiteMetadataRepo,
)
from app.infrastructure.sql.duckdb_engine import DuckDBEngine
from app.services.ingest_service import IngestService
from app.services.rag_service import RAGService
from app.services.sql_service import SQLService

_settings = None
_embedder = None
_index = None
_meta_repo = None
_sql_engine = None
_ingest_service = None
_rag_service = None
_sql_service = None


def get_settings_cached():
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings


def get_embedder():
    global _embedder
    if _embedder is None:
        s = get_settings_cached()
        import os
        env_provider = os.getenv(
            "EMBEDDINGS_PROVIDER", s.EMBEDDINGS_PROVIDER
        )
        provider = env_provider.lower()
        if provider == "openai":
            from app.infrastructure.embeddings import (
                openai_embedder as _openai,
            )
            model = os.getenv(
                "EMBEDDINGS_OPENAI_MODEL", s.EMBEDDINGS_OPENAI_MODEL
            )
            _embedder = _openai.OpenAIEmbedder(model=model)
        elif provider == "random":
            _embedder = RandomEmbedder()
        else:
            try:
                bs = int(
                    os.getenv("EMBEDDINGS_BATCH_SIZE", s.EMBEDDINGS_BATCH_SIZE)
                )
            except Exception:
                bs = s.EMBEDDINGS_BATCH_SIZE
            _embedder = STEmbedder(s.EMBEDDINGS_MODEL, batch_size=bs)
    return _embedder


def get_index():
    global _index
    if _index is None:
        s = get_settings_cached()
        _index = FaissIPIndex(get_embedder().dim, s.INDEX_PATH)
    return _index


def get_meta_repo():
    global _meta_repo
    if _meta_repo is None:
        s = get_settings_cached()
        _meta_repo = SQLiteMetadataRepo(s.META_DB_PATH)
    return _meta_repo


def get_sql_engine():
    global _sql_engine
    if _sql_engine is None:
        _sql_engine = DuckDBEngine()
    return _sql_engine


def get_ingest_service():
    global _ingest_service
    if _ingest_service is None:
        s = get_settings_cached()
        _ingest_service = IngestService(
            s.DATA_DIR,
            get_embedder(),
            get_index(),
            get_meta_repo(),
            get_sql_engine(),
        )
    return _ingest_service


def get_rag_service():
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService(get_embedder(), get_index(), get_meta_repo())
    return _rag_service


def get_sql_service():
    global _sql_service
    if _sql_service is None:
        _sql_service = SQLService(get_sql_engine())
    return _sql_service
