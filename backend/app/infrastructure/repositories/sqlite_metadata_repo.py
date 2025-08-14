import sqlite3
import os
import json

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
  rid INTEGER PRIMARY KEY,
  text TEXT NOT NULL,
  meta TEXT NOT NULL
);
"""


class SQLiteMetadataRepo:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        with sqlite3.connect(self.path) as con:
            con.execute(SCHEMA)

    def upsert_chunk(self, rid: int, text: str, meta: dict) -> None:
        with sqlite3.connect(self.path) as con:
            con.execute(
                (
                    "INSERT OR REPLACE INTO chunks(rid, text, meta) "
                    "VALUES(?, ?, ?)"
                ),
                (rid, text, json.dumps(meta, ensure_ascii=False)),
            )

    def get_chunk_by_rid(self, rid: int):
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "SELECT text, meta FROM chunks WHERE rid=?", (rid,))
            row = cur.fetchone()
        if not row:
            return None
        text, meta_json = row
        return text, json.loads(meta_json)
