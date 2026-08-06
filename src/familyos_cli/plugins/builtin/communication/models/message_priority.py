"""Message priority model."""

from __future__ import annotations

from enum import StrEnum


class MessagePriority(StrEnum):
    """Supported message priorities."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
