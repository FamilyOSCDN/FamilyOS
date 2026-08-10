"""Document decisions."""

from __future__ import annotations

from enum import StrEnum


class DocumentDecision(StrEnum):
    """Possible document decisions."""

    ALLOW = "allow"

    REVIEW = "review"

    DENY = "deny"