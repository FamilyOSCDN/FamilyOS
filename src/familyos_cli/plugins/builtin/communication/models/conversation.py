"""Communication conversation model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from familyos_cli.plugins.builtin.communication.models.communication_channel import (
    CommunicationChannel,
)
from familyos_cli.plugins.builtin.communication.models.message import (
    Message,
)
from familyos_cli.plugins.builtin.communication.models.participant import (
    Participant,
)


@dataclass(frozen=True, slots=True)
class Conversation:
    """Represents a communication conversation."""

    identifier: str
    title: str
    participants: tuple[Participant, ...]
    channel: CommunicationChannel
    messages: tuple[Message, ...] = field(
        default_factory=tuple,
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:
        """Validate conversation."""

        if not self.identifier.strip():
            raise ValueError(
                "Conversation identifier must not be empty."
            )

        if not self.title.strip():
            raise ValueError(
                "Conversation title must not be empty."
            )

        if not self.participants:
            raise ValueError(
                "Conversation must have at least one participant."
            )

        participant_ids = {
            participant.identifier
            for participant in self.participants
        }

        if len(participant_ids) != len(self.participants):
            raise ValueError(
                "Conversation participants must be unique."
            )

        if self.updated_at < self.created_at:
            raise ValueError(
                "Conversation updated_at must not precede created_at."
            )

        for message in self.messages:
            message_participant_ids = {
                message.sender.identifier,
                *(
                    recipient.identifier
                    for recipient in message.recipients
                ),
            }

            if not message_participant_ids.issubset(
                participant_ids,
            ):
                raise ValueError(
                    "Message participants must belong to the conversation."
                )
