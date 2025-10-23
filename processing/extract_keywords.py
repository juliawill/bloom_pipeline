from __future__ import annotations

import re
from typing import Dict, Iterable, List, Sequence

import pandas as pd

DEFAULT_KEYWORDS: Dict[str, Sequence[str]] = {
    "oxidation": ("oxidation", "oxidize", "oxidised", "oxidized"),
    "undertone": ("undertone", "cool tone", "warm tone", "neutral tone"),
    "transfer": ("transfer", "smudge", "smudging"),
    "longevity": ("long lasting", "longevity", "wear time"),
    "coverage": ("coverage", "full coverage", "sheer", "buildable"),
    "finish": ("matte", "dewy", "luminous", "radiant"),
}


def extract_keywords(text: str, keyword_map: Dict[str, Iterable[str]] | None = None) -> List[str]:
    """Return a sorted list of keywords that appear in text."""

    if not text:
        return []

    keyword_map = keyword_map or DEFAULT_KEYWORDS
    lowered = text.lower()
    found = set()

    for canonical, variations in keyword_map.items():
        for variant in variations:
            pattern = r"\b{}\b".format(re.escape(variant.lower()))
            if re.search(pattern, lowered):
                found.add(canonical)
                break

    return sorted(found)


def add_keyword_column(
    df: pd.DataFrame,
    *,
    text_column: str = "clean_text",
    keywords_column: str = "keywords",
    keyword_map: Dict[str, Iterable[str]] | None = None,
) -> pd.DataFrame:
    """Return a copy of df with an additional keywords column."""

    working = df.copy()
    working[keywords_column] = working[text_column].map(lambda text: extract_keywords(text, keyword_map))
    return working


__all__ = ["DEFAULT_KEYWORDS", "add_keyword_column", "extract_keywords"]
