"""Communication channel model."""

from __future__ import annotations

from enum import StrEnum


class CommunicationChannel(StrEnum):
    """Supported communication channels."""

    EMAIL = "email"
    SMS = "sms"
    CHAT = "chat"
    PHONE = "phone"
    VIDEO = "video"
    SOCIAL = "social"
