"""Tests for the Conversation model."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
    Conversation,
    Message,
    Participant,
)


def create_participant(identifier: str) -> Participant:
    return Participant(
        identifier=identifier,
        display_name=identifier.title(),
        address=f"{identifier}@example.com",
    )


def create_message(
    sender: Participant,
    recipient: Participant,
) -> Message:
    return Message(
        identifier="msg-1",
        sender=sender,
        recipients=(recipient,),
        subject="Family update",
        body="This is a family communication.",
    )


def test_conversation_creation() -> None:
    alice = create_participant("alice")
    bob = create_participant("bob")
    message = create_message(alice, bob)

    conversation = Conversation(
        identifier="conversation-1",
        title="Family Updates",
        participants=(
            alice,
            bob,
        ),
        channel=CommunicationChannel.EMAIL,
        messages=(message,),
    )

    assert conversation.identifier == "conversation-1"
    assert conversation.title == "Family Updates"
    assert conversation.channel is CommunicationChannel.EMAIL
    assert conversation.messages == (message,)


def test_conversation_allows_no_messages() -> None:
    participant = create_participant("alice")

    conversation = Conversation(
        identifier="conversation-1",
        title="New Conversation",
        participants=(participant,),
        channel=CommunicationChannel.CHAT,
    )

    assert conversation.messages == ()


def test_conversation_requires_participants() -> None:
    with pytest.raises(
        ValueError,
        match="at least one participant",
    ):
        Conversation(
            identifier="conversation-1",
            title="Empty Conversation",
            participants=(),
            channel=CommunicationChannel.CHAT,
        )


def test_conversation_rejects_duplicate_participants() -> None:
    participant = create_participant("alice")

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        Conversation(
            identifier="conversation-1",
            title="Duplicate Participants",
            participants=(
                participant,
                participant,
            ),
            channel=CommunicationChannel.CHAT,
        )


def test_conversation_rejects_message_from_unknown_participant() -> None:
    alice = create_participant("alice")
    bob = create_participant("bob")
    charlie = create_participant("charlie")
    message = create_message(alice, charlie)

    with pytest.raises(
        ValueError,
        match="must belong to the conversation",
    ):
        Conversation(
            identifier="conversation-1",
            title="Family Updates",
            participants=(
                alice,
                bob,
            ),
            channel=CommunicationChannel.EMAIL,
            messages=(message,),
        )


def test_conversation_rejects_invalid_timestamp_order() -> None:
    participant = create_participant("alice")
    created_at = datetime.now(UTC)
    updated_at = created_at - timedelta(seconds=1)

    with pytest.raises(
        ValueError,
        match="must not precede",
    ):
        Conversation(
            identifier="conversation-1",
            title="Family Updates",
            participants=(participant,),
            channel=CommunicationChannel.CHAT,
            created_at=created_at,
            updated_at=updated_at,
        )


def test_conversation_is_immutable() -> None:
    participant = create_participant("alice")

    conversation = Conversation(
        identifier="conversation-1",
        title="Family Updates",
        participants=(participant,),
        channel=CommunicationChannel.CHAT,
    )

    with pytest.raises(FrozenInstanceError):
        conversation.title = "Changed"  # type: ignore[misc]
