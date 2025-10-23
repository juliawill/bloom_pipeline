from __future__ import annotations

import sys
from typing import Optional

from loguru import logger


def configure_logger(level: str = "INFO") -> None:
    """Configure loguru with a consistent structured output."""

    logger.remove()
    logger.add(
        sys.stdout,
        level=level.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {extra[agent]:<16} | {level:<8} | {message}",
        enqueue=False,
    )


def get_logger(agent_name: Optional[str] = None):
    """Return a logger bound with the agent name for consistent metadata."""

    if not logger._core.handlers:
        configure_logger()

    bound_name = agent_name or "system"
    return logger.bind(agent=bound_name)


__all__ = ["configure_logger", "get_logger"]
