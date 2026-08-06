"""Communication message model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from familyos_cli.plugins.builtin.communication.models.attachment import (
    Attachment,
)
from familyos_cli.plugins.builtin.communication.models.delivery_status import (
    DeliveryStatus,
)
from familyos_cli.plugins.builtin.communication.models.message_priority import (
    MessagePriority,
)
from familyos_cli.plugins.builtin.communication.models.participant import (
    Participant,
)


@dataclass(frozen=True, slots=True)
class Message:
    """Represents a communication message."""

    identifier: str
    sender: Participant
    recipients: tuple[Participant, ...]
    subject: str
    body: str
    priority: MessagePriority = MessagePriority.NORMAL
    status: DeliveryStatus = DeliveryStatus.PENDING
    attachments: tuple[Attachment, ...] = field(
        default_factory=tuple,
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:
        """Validate message."""

        if not self.identifier.strip():
            raise ValueError(
                "Message identifier must not be empty."
            )

        if not self.subject.strip():
            raise ValueError(
                "Message subject must not be empty."
            )

        if not self.body.strip():
            raise ValueError(
                "Message body must not be empty."
            )

        if not self.recipients:
            raise ValueError(
                "Message must have at least one recipient."
            )
