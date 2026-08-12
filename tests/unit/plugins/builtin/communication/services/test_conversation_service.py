"""Tests for ConversationService."""

import pytest

from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
    Message,
    Participant,
)
from familyos_cli.plugins.builtin.communication.repositories import (
    InMemoryCommunicationRepository,
)
from familyos_cli.plugins.builtin.communication.services import (
    ConversationService,
)


def participant(identifier: str) -> Participant:
    """Create a participant."""

    return Participant(
        identifier=identifier,
        display_name=identifier,
        address=f"{identifier}@example.com",
    )


def message(
    sender: Participant,
    recipient: Participant,
) -> Message:
    """Create a message."""

    return Message(
        identifier="msg-1",
        sender=sender,
        recipients=(recipient,),
        subject="Hello",
        body="FamilyOS",
    )


def test_create_conversation() -> None:
    """Service should create a conversation."""

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
    """Service should add a message immutably."""

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
    """Service should add a participant."""

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
    """Service should remove a participant."""

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


def test_service_persists_and_retrieves_conversation() -> None:
    """Service should persist through its repository boundary."""

    repository = InMemoryCommunicationRepository()

    service = ConversationService(
        repository,
    )

    conversation = service.create(
        identifier="conv-1",
        title="Family",
        participants=(participant("alice"),),
        channel=CommunicationChannel.CHAT,
    )

    service.save(
        conversation,
    )

    assert service.exists(
        "conv-1",
    )

    assert service.get(
        "conv-1",
    ) == conversation

    assert service.list() == (
        conversation,
    )


def test_service_persists_updated_conversation() -> None:
    """Service should persist an updated conversation."""

    repository = InMemoryCommunicationRepository()

    service = ConversationService(
        repository,
    )

    alice = participant("alice")
    bob = participant("bob")

    conversation = service.create(
        identifier="conv-1",
        title="Family",
        participants=(alice, bob),
        channel=CommunicationChannel.CHAT,
    )

    service.save(
        conversation,
    )

    updated = service.add_message(
        conversation,
        message(alice, bob),
    )

    service.save(
        updated,
    )

    persisted = service.get(
        "conv-1",
    )

    assert persisted == updated
    assert persisted is not None
    assert len(persisted.messages) == 1


def test_service_deletes_conversation() -> None:
    """Service should delete through its repository boundary."""

    repository = InMemoryCommunicationRepository()

    service = ConversationService(
        repository,
    )

    conversation = service.create(
        identifier="conv-1",
        title="Family",
        participants=(participant("alice"),),
        channel=CommunicationChannel.CHAT,
    )

    service.save(
        conversation,
    )

    service.delete(
        "conv-1",
    )

    assert not service.exists(
        "conv-1",
    )

    assert service.get(
        "conv-1",
    ) is None


def test_repository_operations_require_configuration() -> None:
    """Persistence operations should require a repository."""

    service = ConversationService()

    with pytest.raises(
        RuntimeError,
        match="Conversation repository is not configured",
    ):
        service.list()
