"""Delivery status model."""

from __future__ import annotations

from enum import StrEnum


class DeliveryStatus(StrEnum):
    """Supported delivery states."""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
