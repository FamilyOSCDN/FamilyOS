"""Communication service."""

from __future__ import annotations

from dataclasses import replace

from familyos_cli.plugins.builtin.communication.models import (
    DeliveryStatus,
    Message,
)


class CommunicationService:
    """Application service for communication messages."""

    _ALLOWED_TRANSITIONS: dict[
        DeliveryStatus,
        frozenset[DeliveryStatus],
    ] = {
        DeliveryStatus.PENDING: frozenset(
            {
                DeliveryStatus.SENT,
                DeliveryStatus.FAILED,
            },
        ),
        DeliveryStatus.SENT: frozenset(
            {
                DeliveryStatus.DELIVERED,
                DeliveryStatus.FAILED,
            },
        ),
        DeliveryStatus.DELIVERED: frozenset(
            {
                DeliveryStatus.READ,
            },
        ),
        DeliveryStatus.READ: frozenset(),
        DeliveryStatus.FAILED: frozenset(),
    }

    @classmethod
    def mark_as_sent(
        cls,
        message: Message,
    ) -> Message:
        """Mark a pending message as sent."""

        return cls._transition(
            message,
            DeliveryStatus.SENT,
        )

    @classmethod
    def mark_as_delivered(
        cls,
        message: Message,
    ) -> Message:
        """Mark a sent message as delivered."""

        return cls._transition(
            message,
            DeliveryStatus.DELIVERED,
        )

    @classmethod
    def mark_as_read(
        cls,
        message: Message,
    ) -> Message:
        """Mark a delivered message as read."""

        return cls._transition(
            message,
            DeliveryStatus.READ,
        )

    @classmethod
    def mark_as_failed(
        cls,
        message: Message,
    ) -> Message:
        """Mark a pending or sent message as failed."""

        return cls._transition(
            message,
            DeliveryStatus.FAILED,
        )

    @classmethod
    def can_transition(
        cls,
        message: Message,
        target_status: DeliveryStatus,
    ) -> bool:
        """Return whether a delivery status transition is allowed."""

        return target_status in cls._ALLOWED_TRANSITIONS[
            message.status
        ]

    @classmethod
    def _transition(
        cls,
        message: Message,
        target_status: DeliveryStatus,
    ) -> Message:
        """Apply a valid delivery status transition."""

        if not cls.can_transition(
            message,
            target_status,
        ):
            raise ValueError(
                "Invalid delivery status transition: "
                f"{message.status.value} -> "
                f"{target_status.value}.",
            )

        return replace(
            message,
            status=target_status,
        )
