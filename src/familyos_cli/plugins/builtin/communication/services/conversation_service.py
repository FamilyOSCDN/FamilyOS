"""Conversation service."""

from __future__ import annotations

from dataclasses import replace

from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
    Conversation,
    Message,
    Participant,
)
from familyos_cli.plugins.builtin.communication.repositories import (
    CommunicationRepository,
)


class ConversationService:
    """Application service for conversations."""

    def __init__(
        self,
        repository: CommunicationRepository | None = None,
    ) -> None:
        """Initialize the service with an optional repository."""

        self._repository = repository

    @staticmethod
    def create(
        *,
        identifier: str,
        title: str,
        participants: tuple[Participant, ...],
        channel: CommunicationChannel,
    ) -> Conversation:
        """Create a new conversation."""

        return Conversation(
            identifier=identifier,
            title=title,
            participants=participants,
            channel=channel,
        )

    @staticmethod
    def add_message(
        conversation: Conversation,
        message: Message,
    ) -> Conversation:
        """Return a conversation with one additional message."""

        return replace(
            conversation,
            messages=(
                *conversation.messages,
                message,
            ),
        )

    @staticmethod
    def add_participant(
        conversation: Conversation,
        participant: Participant,
    ) -> Conversation:
        """Return a conversation with one additional participant."""

        if participant in conversation.participants:
            return conversation

        return replace(
            conversation,
            participants=(
                *conversation.participants,
                participant,
            ),
        )

    @staticmethod
    def remove_participant(
        conversation: Conversation,
        participant_id: str,
    ) -> Conversation:
        """Return a conversation without one participant."""

        return replace(
            conversation,
            participants=tuple(
                participant
                for participant in conversation.participants
                if participant.identifier != participant_id
            ),
        )

    def save(
        self,
        conversation: Conversation,
    ) -> None:
        """Persist a conversation."""

        self._require_repository().save(
            conversation,
        )

    def get(
        self,
        identifier: str,
    ) -> Conversation | None:
        """Return a persisted conversation."""

        return self._require_repository().get(
            identifier,
        )

    def list(
        self,
    ) -> tuple[Conversation, ...]:
        """Return all persisted conversations."""

        return self._require_repository().list()

    def delete(
        self,
        identifier: str,
    ) -> None:
        """Delete a persisted conversation."""

        self._require_repository().delete(
            identifier,
        )

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """Return whether a persisted conversation exists."""

        return self._require_repository().exists(
            identifier,
        )

    def _require_repository(
        self,
    ) -> CommunicationRepository:
        """Return the configured repository."""

        if self._repository is None:
            raise RuntimeError(
                "Conversation repository is not configured.",
            )

        return self._repository
