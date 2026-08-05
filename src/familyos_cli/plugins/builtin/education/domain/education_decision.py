"""Education decision model."""

from __future__ import annotations

from enum import StrEnum


class EducationDecision(StrEnum):
    """Possible education decisions."""

    ALLOW = "allow"

    REVIEW = "review"

    DENY = "deny"
