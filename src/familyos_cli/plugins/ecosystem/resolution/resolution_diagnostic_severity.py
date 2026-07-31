"""Plugin resolution diagnostic severities."""

from __future__ import annotations

from enum import StrEnum


class ResolutionDiagnosticSeverity(StrEnum):
    """Represent the severity of a plugin resolution diagnostic."""

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"
