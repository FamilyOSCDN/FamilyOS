"""Document type model."""

from __future__ import annotations

from enum import StrEnum


class DocumentType(StrEnum):
    """Supported document categories."""

    IDENTITY = "identity"
    FINANCE = "finance"
    HEALTH = "health"
    EDUCATION = "education"
    LEGAL = "legal"
    ARCHIVE = "archive"
