"""Tests for CommunicationRepository."""

from inspect import isabstract

from familyos_cli.plugins.builtin.communication.repositories import (
    CommunicationRepository,
)


def test_repository_is_abstract() -> None:
    assert isabstract(
        CommunicationRepository,
    )
