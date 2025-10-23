from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from utils.config import Config
from utils.db import Database
from utils.logging import get_logger


class BaseAgent(ABC):
    """Abstract base class implementing the generic agent lifecycle."""

    def __init__(
        self,
        *,
        config: Config,
        db: Database,
        logger=None,
        think: Optional[Callable[..., Any]] = None,
    ) -> None:
        self.config = config
        self.db = db
        self.logger = logger or get_logger(self.__class__.__name__)
        self.think = think
        self.metrics: Dict[str, Any] = {}
        self.state: Dict[str, Any] = {}

    def run(self) -> None:
        """Execute the standard prepare → act → persist lifecycle."""

        self.logger.info("Starting agent run.")
        try:
            self.prepare()
            self.act()
            self.persist()
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.exception(f"Agent run failed: {exc}")
            raise
        else:
            self.logger.info("Completed agent run.")

    @abstractmethod
    def prepare(self) -> None:
        """Load inputs and prepare resources."""

    @abstractmethod
    def act(self) -> None:
        """Perform the core logic for the agent."""

    @abstractmethod
    def persist(self) -> None:
        """Persist outputs and emit downstream signals."""


__all__ = ["BaseAgent"]
