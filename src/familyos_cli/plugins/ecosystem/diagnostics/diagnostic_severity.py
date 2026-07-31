"""Plugin resolution diagnostic severity levels."""

from __future__ import annotations

from enum import StrEnum


class DiagnosticSeverity(StrEnum):
    """Represent the severity of a plugin resolution diagnostic."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
