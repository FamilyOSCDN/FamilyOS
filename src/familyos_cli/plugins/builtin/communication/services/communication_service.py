"""Communication service."""

from __future__ import annotations

from dataclasses import replace

from familyos_cli.plugins.builtin.communication.models import (
    DeliveryStatus,
    Message,
)


class CommunicationService:
    """Application service for communication messages."""

    @staticmethod
    def mark_as_sent(
        message: Message,
    ) -> Message:
        """Mark a message as sent."""

        return replace(
            message,
            status=DeliveryStatus.SENT,
        )

    @staticmethod
    def mark_as_delivered(
        message: Message,
    ) -> Message:
        """Mark a message as delivered."""

        return replace(
            message,
            status=DeliveryStatus.DELIVERED,
        )

    @staticmethod
    def mark_as_read(
        message: Message,
    ) -> Message:
        """Mark a message as read."""

        return replace(
            message,
            status=DeliveryStatus.READ,
        )

    @staticmethod
    def mark_as_failed(
        message: Message,
    ) -> Message:
        """Mark a message as failed."""

        return replace(
            message,
            status=DeliveryStatus.FAILED,
        )
