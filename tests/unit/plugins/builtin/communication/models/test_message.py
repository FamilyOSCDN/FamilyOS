from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.communication.models import (
    DeliveryStatus,
    Message,
    MessagePriority,
    Participant,
)


def create_participant(identifier: str) -> Participant:
    return Participant(
        identifier=identifier,
        display_name=identifier,
        address=f"{identifier}@example.com",
    )


def test_message_creation() -> None:
    sender = create_participant("alice")
    recipient = create_participant("bob")

    message = Message(
        identifier="msg-1",
        sender=sender,
        recipients=(recipient,),
        subject="Hello",
        body="Welcome to FamilyOS",
    )

    assert message.identifier == "msg-1"
    assert message.priority is MessagePriority.NORMAL
    assert message.status is DeliveryStatus.PENDING
    assert len(message.recipients) == 1


def test_message_requires_recipients() -> None:
    sender = create_participant("alice")

    with pytest.raises(ValueError):
        Message(
            identifier="msg-1",
            sender=sender,
            recipients=(),
            subject="Hello",
            body="Body",
        )


def test_message_is_immutable() -> None:
    sender = create_participant("alice")
    recipient = create_participant("bob")

    message = Message(
        identifier="msg-1",
        sender=sender,
        recipients=(recipient,),
        subject="Hello",
        body="Body",
    )

    with pytest.raises(FrozenInstanceError):
        message.subject = "New subject"  # type: ignore[misc]
