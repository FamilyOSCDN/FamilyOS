"""Compliance finding categories."""

from __future__ import annotations

from enum import StrEnum


class FindingCategory(StrEnum):
    """Categorize the meaning of a compliance finding."""

    VIOLATION = "violation"
    INCOMPLETE = "incomplete"
    VALIDATION_ERROR = "validation_error"
    GOVERNANCE = "governance"
    ADVISORY = "advisory"
