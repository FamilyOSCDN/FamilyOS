"""Conversation service."""

from __future__ import annotations

from dataclasses import replace

from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
    Conversation,
    Message,
    Participant,
)


class ConversationService:
    """Application service for conversations."""

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
