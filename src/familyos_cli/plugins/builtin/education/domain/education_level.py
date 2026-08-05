"""Education level model."""

from __future__ import annotations

from enum import StrEnum


class EducationLevel(StrEnum):
    """Education maturity levels."""

    BASIC = "basic"

    STANDARD = "standard"

    ADVANCED = "advanced"

    CRITICAL = "critical"
