from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.communication.models import (
    Participant,
)


def test_participant_creation() -> None:
    participant = Participant(
        identifier="user-1",
        display_name="Alice",
        address="alice@example.com",
    )

    assert participant.identifier == "user-1"
    assert participant.display_name == "Alice"
    assert participant.address == "alice@example.com"


def test_participant_rejects_empty_fields() -> None:
    with pytest.raises(ValueError):
        Participant(
            identifier="",
            display_name="Alice",
            address="alice@example.com",
        )


def test_participant_is_immutable() -> None:
    participant = Participant(
        identifier="user-1",
        display_name="Alice",
        address="alice@example.com",
    )

    with pytest.raises(FrozenInstanceError):
        participant.display_name = "Bob"  # type: ignore[misc]
