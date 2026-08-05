"""Finance decisions."""

from __future__ import annotations

from enum import StrEnum


class FinanceDecision(StrEnum):
    """Possible finance decisions."""

    ALLOW = "allow"

    REVIEW = "review"

    DENY = "deny"
