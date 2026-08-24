"""Clock authority for canonical Testing Framework evidence."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class TestingClockPort(ABC):
    """Provide current time without exposing system clock details."""

    @abstractmethod
    def now(self) -> datetime:
        """Return the current timezone-aware timestamp."""

        raise NotImplementedError
