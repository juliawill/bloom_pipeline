from __future__ import annotations

from typing import Optional

import pandas as pd

from agents.base import BaseAgent
from processing.clean_reviews import clean_reviews
from processing.extract_keywords import add_keyword_column
from utils.config import Config
from utils.db import Database
from utils.logging import get_logger


class CleaningAgent(BaseAgent):
    """Agent responsible for cleaning and enriching raw review data."""

    def __init__(
        self,
        *,
        config: Config,
        db: Database,
        logger=None,
        think=None,
        raw_table: Optional[str] = None,
        clean_table: Optional[str] = None,
    ) -> None:
        super().__init__(config=config, db=db, logger=logger or get_logger("CleaningAgent"), think=think)
        self.raw_table = raw_table or config.raw_reviews_table
        self.clean_table = clean_table or config.clean_reviews_table
        self.raw_reviews: Optional[pd.DataFrame] = None
        self.cleaned_reviews: Optional[pd.DataFrame] = None

    def prepare(self) -> None:
        self.logger.info(f"Loading raw reviews from {self.raw_table}.")
        self.raw_reviews = self.db.read_table(self.raw_table)
        self.logger.info(f"Loaded {len(self.raw_reviews)} raw rows.")

    def act(self) -> None:
        if self.raw_reviews is None:
            raise RuntimeError("prepare() must be called before act().")

        cleaned, metrics = clean_reviews(
            self.raw_reviews,
            text_column="review_text",
            language_column="language" if "language" in self.raw_reviews.columns else None,
            source_id_column="id" if "id" in self.raw_reviews.columns else None,
        )
        enriched = add_keyword_column(cleaned)
        self.cleaned_reviews = enriched

        self.metrics.update(metrics)
        self.metrics["keywords_populated"] = int(enriched["keywords"].map(bool).sum())
        self.logger.info(
            "Cleaning complete. Rows: {row_count}, invalid removed: {invalid_rows_removed}, "
            "language filtered: {language_filtered}, duplicates removed: {duplicates_removed}.",
            **self.metrics,
        )

    def persist(self) -> None:
        if self.cleaned_reviews is None:
            raise RuntimeError("act() must be called before persist().")

        if self.cleaned_reviews.empty:
            self.logger.warning("No cleaned reviews to persist; skipping database write.")
            return

        self.logger.info(f"Writing {len(self.cleaned_reviews)} cleaned reviews to {self.clean_table}.")
        self.db.write_dataframe(self.cleaned_reviews, self.clean_table, if_exists="replace")
        self.logger.info("Persisted cleaned reviews successfully.")


__all__ = ["CleaningAgent"]
