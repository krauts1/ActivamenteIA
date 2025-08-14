import pandas as pd
from app.domain.ports import SQLEngine


class SQLService:
    def __init__(self, engine: SQLEngine):
        self.engine = engine

    def preview(self, limit: int = 50) -> pd.DataFrame:
        return self.engine.sample_preview(limit)

    def run(self, sql: str, limit: int = 200) -> pd.DataFrame:
        return self.engine.safe_query(sql, limit)
