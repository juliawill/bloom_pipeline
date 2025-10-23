from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from utils.config import Config


@dataclass
class Database:
    """Simple SQLAlchemy wrapper for loading and persisting tabular data."""

    engine: Engine

    @classmethod
    def from_config(cls, config: Config, *, echo: bool = False) -> "Database":
        engine = create_engine(config.database.uri, echo=echo, future=True)
        return cls(engine=engine)

    @staticmethod
    def _split_table_name(table_name: str) -> Tuple[Optional[str], str]:
        if "." in table_name:
            schema, table = table_name.split(".", 1)
            return schema, table
        return None, table_name

    @staticmethod
    def _quote(identifier: str) -> str:
        escaped = identifier.replace('"', '""')
        return f'"{escaped}"'

    def read_table(self, table_name: str, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
        schema, table = self._split_table_name(table_name)
        qualified = self._quote(table)
        if schema:
            qualified = f"{self._quote(schema)}.{qualified}"

        if columns:
            col_clause = ", ".join(self._quote(col) for col in columns)
        else:
            col_clause = "*"

        query = text(f"SELECT {col_clause} FROM {qualified}")
        return pd.read_sql_query(query, self.engine)

    def write_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        *,
        if_exists: str = "replace",
        chunksize: Optional[int] = None,
    ) -> None:
        schema, table = self._split_table_name(table_name)
        df_to_write = self._prepare_for_persistence(df)
        df_to_write.to_sql(
            name=table,
            con=self.engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize,
            method="multi",
        )

    def _prepare_for_persistence(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare dataframe for insertion depending on the destination dialect."""

        if self.engine.dialect.name != "sqlite":
            return df

        # SQLite cannot store lists directly; serialize list-like objects to JSON.
        import json

        df_copy = df.copy()
        for column in df_copy.columns:
            if df_copy[column].map(lambda value: isinstance(value, (list, tuple, dict))).any():
                df_copy[column] = df_copy[column].map(
                    lambda value: None
                    if value is None or value is pd.NA
                    else json.dumps(value)
                )
        return df_copy

    def execute(self, statement: str, **params) -> None:
        with self.engine.begin() as connection:
            connection.execute(text(statement), params)

    @contextmanager
    def transaction(self):
        with self.engine.begin() as connection:
            yield connection

    def dispose(self) -> None:
        self.engine.dispose()


__all__ = ["Database"]
