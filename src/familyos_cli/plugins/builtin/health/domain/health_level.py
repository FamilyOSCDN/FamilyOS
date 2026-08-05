"""Health security level model."""

from __future__ import annotations

from enum import StrEnum


class HealthLevel(StrEnum):
    """Represents health criticality levels."""

    BASIC = "basic"

    STANDARD = "standard"

    ADVANCED = "advanced"

    CRITICAL = "critical"
