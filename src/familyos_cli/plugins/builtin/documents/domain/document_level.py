"""Document security levels."""

from __future__ import annotations

from enum import StrEnum


class DocumentLevel(StrEnum):
    """Represents document criticality levels."""

    BASIC = "basic"

    STANDARD = "standard"

    SENSITIVE = "sensitive"

    CRITICAL = "critical"