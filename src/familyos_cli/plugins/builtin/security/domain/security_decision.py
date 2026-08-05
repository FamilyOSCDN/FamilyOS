"""Security decision value object."""

from __future__ import annotations

from enum import StrEnum


class SecurityDecision(StrEnum):
    """Represents the result of a security evaluation."""

    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"
