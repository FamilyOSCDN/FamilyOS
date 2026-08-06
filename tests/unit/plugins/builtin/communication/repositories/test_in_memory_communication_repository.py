"""Tests for InMemoryCommunicationRepository."""

from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
    Conversation,
    Participant,
)
from familyos_cli.plugins.builtin.communication.repositories import (
    InMemoryCommunicationRepository,
)


def participant(identifier: str) -> Participant:
    return Participant(
        identifier=identifier,
        display_name=identifier.title(),
        address=f"{identifier}@example.com",
    )


def conversation() -> Conversation:
    alice = participant("alice")

    return Conversation(
        identifier="conversation-1",
        title="Family",
        participants=(alice,),
        channel=CommunicationChannel.CHAT,
    )


def test_save_and_get() -> None:
    repository = (
        InMemoryCommunicationRepository()
    )

    item = conversation()

    repository.save(item)

    assert (
        repository.get(
            item.identifier,
        )
        == item
    )


def test_exists() -> None:
    repository = (
        InMemoryCommunicationRepository()
    )

    item = conversation()

    repository.save(item)

    assert repository.exists(
        item.identifier,
    )

    assert not repository.exists(
        "unknown",
    )


def test_list() -> None:
    repository = (
        InMemoryCommunicationRepository()
    )

    item = conversation()

    repository.save(item)

    conversations = repository.list()

    assert len(conversations) == 1

    assert conversations[0] == item


def test_delete() -> None:
    repository = (
        InMemoryCommunicationRepository()
    )

    item = conversation()

    repository.save(item)

    repository.delete(
        item.identifier,
    )

    assert repository.get(
        item.identifier,
    ) is None
