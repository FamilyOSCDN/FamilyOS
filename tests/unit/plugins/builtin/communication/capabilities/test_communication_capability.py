"""Tests for CommunicationCapability."""

from familyos_cli.plugins.builtin.communication.capabilities.communication_capability import (
    CommunicationCapability,
)


def test_communication_capability_has_expected_identifier() -> None:
    capability = CommunicationCapability.create()

    assert str(
        capability.id,
    ) == "familyos.communication.messaging"


def test_communication_capability_has_expected_metadata() -> None:
    capability = CommunicationCapability.create()

    assert capability.display_name == (
        "Communication"
    )

    assert (
        "communication management"
        in capability.description
    )

    assert capability.metadata["domain"] == (
        "communication"
    )

    assert capability.metadata["version"] == (
        "1.0.0"
    )
