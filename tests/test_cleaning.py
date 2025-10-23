from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from agents.cleaning_agent import CleaningAgent
from processing.clean_reviews import clean_reviews, normalize_text
from processing.extract_keywords import add_keyword_column, extract_keywords
from utils.config import Config, DatabaseConfig
from utils.db import Database


def make_raw_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"id": 1, "review_text": "I LOVE this product! Great finish.", "language": "en"},
            {"id": 2, "review_text": "This foundation oxidizes fast.", "language": "en"},
            {"id": 3, "review_text": "This foundation oxidizes fast!!!", "language": "en"},
            {"id": 4, "review_text": None, "language": "en"},
            {"id": 5, "review_text": "Me encanta este producto", "language": "es"},
        ]
    )


def test_normalize_text_removes_noise():
    raw = "Glowy Finish!!!  "
    assert normalize_text(raw) == "glowy finish"


def test_clean_reviews_filters_invalid_and_duplicates():
    raw_df = make_raw_dataframe()

    cleaned, metrics = clean_reviews(raw_df)

    assert len(cleaned) == 2
    assert set(cleaned["clean_text"]) == {
        "i love this product great finish",
        "this foundation oxidizes fast",
    }
    assert metrics["invalid_rows_removed"] == 1
    assert metrics["language_filtered"] == 1
    assert metrics["duplicates_removed"] == 1


def test_extract_keywords_matches_expected_terms():
    text = "The luminous finish is beautiful but it oxidized fast."
    assert extract_keywords(text) == ["finish", "oxidation"]

    df = pd.DataFrame([{"clean_text": text}])
    enriched = add_keyword_column(df)
    assert enriched.at[0, "keywords"] == ["finish", "oxidation"]


def test_cleaning_agent_runs_full_pipeline():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db = Database(engine=engine)

    config = Config(
        environment="test",
        log_level="INFO",
        database=DatabaseConfig(uri="sqlite+pysqlite:///:memory:"),
        raw_reviews_table="raw_reviews",
        clean_reviews_table="clean_reviews",
    )

    make_raw_dataframe().to_sql("raw_reviews", con=engine, index=False, if_exists="replace")

    agent = CleaningAgent(config=config, db=db)
    agent.run()

    assert agent.cleaned_reviews is not None
    assert len(agent.cleaned_reviews) == 2
    assert agent.metrics["duplicates_removed"] == 1

    persisted = db.read_table("clean_reviews")
    assert len(persisted) == 2
    assert "clean_text" in persisted.columns
