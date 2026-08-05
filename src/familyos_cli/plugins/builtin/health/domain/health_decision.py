"""Health decision model."""

from __future__ import annotations

from enum import StrEnum


class HealthDecision(StrEnum):
    """Represents health evaluation decisions."""

    ALLOW = "allow"

    REVIEW = "review"

    DENY = "deny"
