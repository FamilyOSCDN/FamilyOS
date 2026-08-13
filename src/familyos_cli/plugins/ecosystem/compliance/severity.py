"""Compliance rule severity levels."""

from __future__ import annotations

from enum import StrEnum


class Severity(StrEnum):
    """Represent the severity of a compliance rule."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
