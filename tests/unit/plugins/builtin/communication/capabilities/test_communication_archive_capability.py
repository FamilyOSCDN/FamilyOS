"""Tests for CommunicationArchiveCapability."""

from familyos_cli.plugins.builtin.communication.capabilities.communication_archive_capability import (
    CommunicationArchiveCapability,
)


def test_communication_archive_capability_has_expected_identifier() -> None:
    capability = CommunicationArchiveCapability.create()

    assert str(
        capability.id,
    ) == "familyos.communication.archive"


def test_communication_archive_capability_has_expected_metadata() -> None:
    capability = CommunicationArchiveCapability.create()

    assert capability.display_name == (
        "Communication Archive"
    )

    assert (
        "communication archive"
        in capability.description
    )

    assert capability.metadata["domain"] == (
        "communication"
    )

    assert capability.metadata["version"] == (
        "1.0.0"
    )
