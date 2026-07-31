"""Plugin conflict reasons."""

from __future__ import annotations

from enum import StrEnum


class ConflictReason(StrEnum):
    """Identify the technical cause of a plugin resolution conflict."""

    INCOMPATIBLE_CONSTRAINTS = "incompatible_constraints"
    NO_COMPATIBLE_VERSION = "no_compatible_version"
    PACKAGE_NOT_FOUND = "package_not_found"
    INVALID_VERSION = "invalid_version"
