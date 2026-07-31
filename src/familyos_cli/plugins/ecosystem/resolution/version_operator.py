"""Version comparison operators."""

from __future__ import annotations

from enum import StrEnum


class VersionOperator(StrEnum):
    """Supported plugin version comparison operators."""

    EQUAL = "=="

    GREATER = ">"

    GREATER_OR_EQUAL = ">="

    LOWER = "<"

    LOWER_OR_EQUAL = "<="

    COMPATIBLE = "^"

    APPROXIMATE = "~"
