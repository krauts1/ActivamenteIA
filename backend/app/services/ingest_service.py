from pathlib import Path
import os
from app.utils.chunking import chunk_text
from app.utils.pdf_parser import iter_text_from_pdf
from app.domain.ports import (
    Embedder,
    VectorIndex,
    MetadataRepository,
    SQLEngine,
)


class IngestService:
    def __init__(
            self,
            data_dir: str,
            embedder: Embedder,
            index: VectorIndex,
            meta_repo: MetadataRepository,
            sql: SQLEngine):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / 'raw').mkdir(parents=True, exist_ok=True)
        self.embedder = embedder
        self.index = index
        self.meta_repo = meta_repo
        self.sql = sql
        self.max_pages = int(os.getenv("MAX_PDF_PAGES", "20"))
        self.max_total_chunks = int(os.getenv("MAX_TOTAL_CHUNKS", "500"))

    def save_raw(self, filename: str, content) -> str:
        path = self.data_dir / 'raw' / filename
        with open(path, 'wb') as f:
            f.write(content)
        return str(path)

    def _embed_and_index(self, chunks, filename: str, batch: int = 4):
        buffer, total = [], 0
        for ch in chunks:
            buffer.append(ch)
            total += 1
            if total >= self.max_total_chunks:
                break
            if len(buffer) >= batch:
                V = self.embedder.encode_batch(buffer)
                ids = self.index.add(V)
                for rid, txt in zip(ids, buffer):
                    self.meta_repo.upsert_chunk(
                        rid, txt, {"filename": filename})
                buffer.clear()
        if buffer:
            V = self.embedder.encode_batch(buffer)
            ids = self.index.add(V)
            for rid, txt in zip(ids, buffer):
                self.meta_repo.upsert_chunk(rid, txt, {"filename": filename})

    def ingest_file(self, filename: str, content: bytes) -> tuple[bool, bool]:
        path = self.save_raw(filename, content)
        registered_in_sql = False
        lower = filename.lower()

        if lower.endswith('.csv'):
            self.sql.register_csv(path)
            registered_in_sql = True
            return True, registered_in_sql

        if lower.endswith(('.txt', '.md')):
            text = Path(path).read_text(encoding='utf-8', errors='ignore')
            if text.strip():
                chunks = chunk_text(text, max_chars=900, overlap=100)
                self._embed_and_index(chunks, filename, batch=4)
                self.index.save()
            return True, registered_in_sql

        if lower.endswith('.pdf'):
            page_count = 0
            total_chunks = 0
            for page_no, page_text in iter_text_from_pdf(path):
                page_count += 1
                if page_count > self.max_pages:
                    break
                if not page_text.strip():
                    continue
                chunks = chunk_text(page_text, max_chars=900, overlap=100)
                remaining = self.max_total_chunks - total_chunks
                if remaining <= 0:
                    break
                if len(chunks) > remaining:
                    chunks = chunks[:remaining]
                self._embed_and_index(chunks, filename, batch=4)
                total_chunks += len(chunks)
            self.index.save()
            return True, registered_in_sql

        raise ValueError('Formato no soportado (PDF/TXT/MD/CSV)')
