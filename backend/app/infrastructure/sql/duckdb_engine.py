import duckdb
import os
import pandas as pd


class DuckDBEngine:
    def __init__(self):
        self.con = duckdb.connect(database=':memory:')

    def register_csv(self, path: str) -> str:
        name = os.path.splitext(os.path.basename(path))[0]
        safe = "csv_" + "".join(ch for ch in name.lower()
                                if ch.isalnum() or ch == "_")
        self.con.execute(
            (
                f"CREATE OR REPLACE VIEW {safe} AS SELECT * FROM "
                f"read_csv_auto('{path}', header=True)"
            )
        )
        return safe

    def safe_query(self, sql: str, limit: int = 200) -> pd.DataFrame:
        s = sql.lower()
        banned = [
            "insert",
            "update",
            "delete",
            "attach",
            "copy",
            "pragma",
            "drop",
            "alter"]
        if any(b in s for b in banned):
            raise ValueError("Operación no permitida")
        if "limit" not in s:
            sql = sql.rstrip(';') + f" LIMIT {int(limit)}"
        return self.con.execute(sql).fetchdf()

    def sample_preview(self, limit: int = 50):
        tables = self.con.execute("SHOW ALL TABLES").fetchdf()
        if tables.empty:
            return pd.DataFrame()
        t = tables.iloc[0]['name']
        return self.con.execute(
            f"SELECT * FROM {t} LIMIT {int(limit)}").fetchdf()
