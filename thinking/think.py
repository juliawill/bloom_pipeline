from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class Thinker:
    """Simple mockable GPT wrapper placeholder."""

    def __init__(self, *, mock_response: Optional[str] = None) -> None:
        self.mock_response = mock_response

    def __call__(self, prompt: str, **_: Any) -> str:
        if self.mock_response is not None:
            return self.mock_response
        raise RuntimeError("think() requires GPT integration or a mock response.")


def think(prompt: str, **kwargs: Any) -> str:
    """Default think function delegating to a mockable Thinker."""

    thinker = kwargs.pop("thinker", None)
    if isinstance(thinker, Thinker):
        return thinker(prompt, **kwargs)
    raise RuntimeError("No Thinker provided; configure GPT integration before use.")


__all__ = ["Thinker", "think"]
