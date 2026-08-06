"""Tests for CommunicationService."""

from familyos_cli.plugins.builtin.communication.models import (
    DeliveryStatus,
    Message,
    Participant,
)
from familyos_cli.plugins.builtin.communication.services import (
    CommunicationService,
)


def create_participant(identifier: str) -> Participant:
    return Participant(
        identifier=identifier,
        display_name=identifier.title(),
        address=f"{identifier}@example.com",
    )


def create_message() -> Message:
    sender = create_participant("alice")
    recipient = create_participant("bob")

    return Message(
        identifier="message-1",
        sender=sender,
        recipients=(recipient,),
        subject="Hello",
        body="Welcome to FamilyOS.",
    )


def test_mark_as_sent() -> None:
    message = create_message()

    updated = CommunicationService.mark_as_sent(
        message,
    )

    assert updated.status is DeliveryStatus.SENT
    assert message.status is DeliveryStatus.PENDING


def test_mark_as_delivered() -> None:
    message = create_message()

    updated = CommunicationService.mark_as_delivered(
        message,
    )

    assert updated.status is DeliveryStatus.DELIVERED


def test_mark_as_read() -> None:
    message = create_message()

    updated = CommunicationService.mark_as_read(
        message,
    )

    assert updated.status is DeliveryStatus.READ


def test_mark_as_failed() -> None:
    message = create_message()

    updated = CommunicationService.mark_as_failed(
        message,
    )

    assert updated.status is DeliveryStatus.FAILED
