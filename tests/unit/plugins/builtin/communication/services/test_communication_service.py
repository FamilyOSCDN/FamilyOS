"""Tests for CommunicationService."""

import pytest

from familyos_cli.plugins.builtin.communication.models import (
    DeliveryStatus,
    Message,
    Participant,
)
from familyos_cli.plugins.builtin.communication.services import (
    CommunicationService,
)


def create_participant(
    identifier: str,
) -> Participant:
    """Create a participant."""

    return Participant(
        identifier=identifier,
        display_name=identifier.title(),
        address=f"{identifier}@example.com",
    )


def create_message(
    *,
    status: DeliveryStatus = DeliveryStatus.PENDING,
) -> Message:
    """Create a message with a delivery status."""

    sender = create_participant("alice")
    recipient = create_participant("bob")

    return Message(
        identifier="message-1",
        sender=sender,
        recipients=(recipient,),
        subject="Hello",
        body="Welcome to FamilyOS.",
        status=status,
    )


def test_mark_as_sent() -> None:
    """Pending messages should transition to sent."""

    message = create_message()

    updated = CommunicationService.mark_as_sent(
        message,
    )

    assert updated.status is DeliveryStatus.SENT
    assert message.status is DeliveryStatus.PENDING


def test_mark_as_delivered() -> None:
    """Sent messages should transition to delivered."""

    message = create_message(
        status=DeliveryStatus.SENT,
    )

    updated = CommunicationService.mark_as_delivered(
        message,
    )

    assert updated.status is DeliveryStatus.DELIVERED


def test_mark_as_read() -> None:
    """Delivered messages should transition to read."""

    message = create_message(
        status=DeliveryStatus.DELIVERED,
    )

    updated = CommunicationService.mark_as_read(
        message,
    )

    assert updated.status is DeliveryStatus.READ


@pytest.mark.parametrize(
    "status",
    (
        DeliveryStatus.PENDING,
        DeliveryStatus.SENT,
    ),
)
def test_mark_as_failed(
    status: DeliveryStatus,
) -> None:
    """Pending and sent messages should transition to failed."""

    message = create_message(
        status=status,
    )

    updated = CommunicationService.mark_as_failed(
        message,
    )

    assert updated.status is DeliveryStatus.FAILED


@pytest.mark.parametrize(
    (
        "current_status",
        "target_status",
    ),
    (
        (
            DeliveryStatus.PENDING,
            DeliveryStatus.DELIVERED,
        ),
        (
            DeliveryStatus.PENDING,
            DeliveryStatus.READ,
        ),
        (
            DeliveryStatus.SENT,
            DeliveryStatus.READ,
        ),
        (
            DeliveryStatus.DELIVERED,
            DeliveryStatus.SENT,
        ),
        (
            DeliveryStatus.DELIVERED,
            DeliveryStatus.FAILED,
        ),
        (
            DeliveryStatus.READ,
            DeliveryStatus.SENT,
        ),
        (
            DeliveryStatus.READ,
            DeliveryStatus.FAILED,
        ),
        (
            DeliveryStatus.FAILED,
            DeliveryStatus.SENT,
        ),
    ),
)
def test_invalid_delivery_status_transitions_are_rejected(
    current_status: DeliveryStatus,
    target_status: DeliveryStatus,
) -> None:
    """Invalid delivery lifecycle transitions should be rejected."""

    message = create_message(
        status=current_status,
    )

    transition = {
        DeliveryStatus.SENT: (
            CommunicationService.mark_as_sent
        ),
        DeliveryStatus.DELIVERED: (
            CommunicationService.mark_as_delivered
        ),
        DeliveryStatus.READ: (
            CommunicationService.mark_as_read
        ),
        DeliveryStatus.FAILED: (
            CommunicationService.mark_as_failed
        ),
    }[target_status]

    with pytest.raises(
        ValueError,
        match=(
            "Invalid delivery status transition: "
            f"{current_status.value} -> "
            f"{target_status.value}"
        ),
    ):
        transition(
            message,
        )


def test_can_transition_reports_valid_transition() -> None:
    """Transition queries should expose valid lifecycle progression."""

    message = create_message(
        status=DeliveryStatus.SENT,
    )

    assert CommunicationService.can_transition(
        message,
        DeliveryStatus.DELIVERED,
    )


def test_can_transition_reports_invalid_transition() -> None:
    """Transition queries should reject invalid lifecycle progression."""

    message = create_message(
        status=DeliveryStatus.PENDING,
    )

    assert not CommunicationService.can_transition(
        message,
        DeliveryStatus.READ,
    )


def test_read_status_is_terminal() -> None:
    """Read messages should not allow further transitions."""

    message = create_message(
        status=DeliveryStatus.READ,
    )

    for target_status in DeliveryStatus:
        assert not CommunicationService.can_transition(
            message,
            target_status,
        )


def test_failed_status_is_terminal() -> None:
    """Failed messages should not allow further transitions."""

    message = create_message(
        status=DeliveryStatus.FAILED,
    )

    for target_status in DeliveryStatus:
        assert not CommunicationService.can_transition(
            message,
            target_status,
        )
