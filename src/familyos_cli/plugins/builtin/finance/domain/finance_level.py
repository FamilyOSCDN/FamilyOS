"""Finance security levels."""

from __future__ import annotations

from enum import StrEnum


class FinanceLevel(StrEnum):
    """Represents finance criticality levels."""

    BASIC = "basic"

    STANDARD = "standard"

    SENSITIVE = "sensitive"

    CRITICAL = "critical"
