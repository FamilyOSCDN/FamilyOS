"""System-backed clock for canonical Testing Framework evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from familyos_cli.application.ports.testing import TestingClockPort


@dataclass(frozen=True, slots=True)
class SystemTestingClock(TestingClockPort):
    """Provide current UTC time from the system clock."""

    def now(self) -> datetime:
        """Return the current timezone-aware UTC timestamp."""

        return datetime.now(UTC)
