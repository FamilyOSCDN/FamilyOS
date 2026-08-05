"""Security level value object."""

from __future__ import annotations

from enum import StrEnum


class SecurityLevel(StrEnum):
    """Represents security criticality levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
