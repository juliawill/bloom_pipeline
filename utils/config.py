from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration details."""

    uri: str


@dataclass(frozen=True)
class Config:
    """Global configuration container used by agents and utilities."""

    environment: str
    log_level: str
    database: DatabaseConfig
    raw_reviews_table: str
    clean_reviews_table: str


def _env(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable '{key}' and no default provided.")
    return value


@lru_cache(maxsize=1)
def get_config() -> Config:
    """Load configuration from environment variables, caching the result."""

    environment = os.getenv("APP_ENV", "development")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    database_uri = _env(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/bloom",
    )
    raw_reviews_table = os.getenv("RAW_REVIEWS_TABLE", "bloom_raw.reviews")
    clean_reviews_table = os.getenv("CLEAN_REVIEWS_TABLE", "bloom_core.reviews_clean")

    return Config(
        environment=environment,
        log_level=log_level,
        database=DatabaseConfig(uri=database_uri),
        raw_reviews_table=raw_reviews_table,
        clean_reviews_table=clean_reviews_table,
    )


__all__ = ["Config", "DatabaseConfig", "get_config"]
