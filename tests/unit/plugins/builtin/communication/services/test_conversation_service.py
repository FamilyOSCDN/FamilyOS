"""Tests for ConversationService."""

from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
    Message,
    Participant,
)
from familyos_cli.plugins.builtin.communication.services import (
    ConversationService,
)


def participant(identifier: str) -> Participant:
    return Participant(
        identifier=identifier,
        display_name=identifier,
        address=f"{identifier}@example.com",
    )


def message(
    sender: Participant,
    recipient: Participant,
) -> Message:
    return Message(
        identifier="msg-1",
        sender=sender,
        recipients=(recipient,),
        subject="Hello",
        body="FamilyOS",
    )


def test_create_conversation() -> None:
    alice = participant("alice")

    conversation = ConversationService.create(
        identifier="conv-1",
        title="Family",
        participants=(alice,),
        channel=CommunicationChannel.CHAT,
    )

    assert conversation.identifier == "conv-1"
    assert len(conversation.participants) == 1


def test_add_message() -> None:
    alice = participant("alice")
    bob = participant("bob")

    conversation = ConversationService.create(
        identifier="conv",
        title="Family",
        participants=(alice, bob),
        channel=CommunicationChannel.CHAT,
    )

    updated = ConversationService.add_message(
        conversation,
        message(alice, bob),
    )

    assert len(updated.messages) == 1
    assert len(conversation.messages) == 0


def test_add_participant() -> None:
    alice = participant("alice")
    bob = participant("bob")

    conversation = ConversationService.create(
        identifier="conv",
        title="Family",
        participants=(alice,),
        channel=CommunicationChannel.CHAT,
    )

    updated = ConversationService.add_participant(
        conversation,
        bob,
    )

    assert len(updated.participants) == 2


def test_remove_participant() -> None:
    alice = participant("alice")
    bob = participant("bob")

    conversation = ConversationService.create(
        identifier="conv",
        title="Family",
        participants=(alice, bob),
        channel=CommunicationChannel.CHAT,
    )

    updated = ConversationService.remove_participant(
        conversation,
        "bob",
    )

    assert len(updated.participants) == 1
