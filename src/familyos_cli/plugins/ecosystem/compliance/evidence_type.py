"""Compliance evidence types."""

from __future__ import annotations

from enum import StrEnum


class EvidenceType(StrEnum):
    """Categorize compliance evidence by its subject matter."""

    IDENTITY = "identity"
    METADATA = "metadata"
    STRUCTURE = "structure"
    ARCHITECTURE = "architecture"
    CAPABILITY = "capability"
    DEPENDENCY = "dependency"
