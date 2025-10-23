from __future__ import annotations

import re
import unicodedata
from typing import Dict, Optional, Tuple

import pandas as pd

PUNCTUATION_PATTERN = re.compile(r"[^\w\s]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Normalize raw review text."""

    if not isinstance(text, str):
        return ""

    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.lower()
    normalized = PUNCTUATION_PATTERN.sub(" ", normalized)
    normalized = WHITESPACE_PATTERN.sub(" ", normalized).strip()
    return normalized


def remove_non_english_characters(text: str) -> str:
    """Remove tokens that look non-English while retaining basic punctuation."""

    if not text:
        return ""

    tokens = [token for token in text.split() if re.fullmatch(r"[a-z0-9']+", token)]
    return " ".join(tokens)


def clean_reviews(
    df: pd.DataFrame,
    *,
    text_column: str = "review_text",
    language_column: Optional[str] = "language",
    source_id_column: Optional[str] = "id",
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Clean, filter, and de-duplicate reviews.

    Returns a tuple of (clean_dataframe, metrics).
    """

    working = df.copy()
    original_count = len(working)

    if text_column not in working.columns:
        raise KeyError(f"Expected column '{text_column}' to exist in dataframe.")

    working[text_column] = working[text_column].fillna("").astype(str)
    working["clean_text"] = working[text_column].map(normalize_text)
    working["clean_text"] = working["clean_text"].map(remove_non_english_characters)

    working = working[working["clean_text"].str.len() >= 5]
    after_filters_count = len(working)

    if language_column and language_column in working.columns:
        english_mask = working[language_column].fillna("").str.lower().str.startswith("en")
        working = working[english_mask]

    before_dedupe_count = len(working)
    working = working.drop_duplicates(subset=["clean_text"])
    after_dedupe_count = len(working)
    duplicates_removed = max(before_dedupe_count - after_dedupe_count, 0)

    if source_id_column and source_id_column in working.columns:
        working = working.rename(columns={source_id_column: "source_id"})
    else:
        working["source_id"] = pd.NA

    metrics = {
        "input_rows": int(original_count),
        "row_count": int(len(working)),
        "invalid_rows_removed": int(original_count - after_filters_count),
        "language_filtered": int(after_filters_count - before_dedupe_count),
        "duplicates_removed": int(duplicates_removed),
    }

    return working.reset_index(drop=True), metrics


__all__ = ["clean_reviews", "normalize_text"]
