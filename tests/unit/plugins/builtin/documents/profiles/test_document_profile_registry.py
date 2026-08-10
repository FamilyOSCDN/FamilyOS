"""Tests for DocumentProfileRegistry."""

from familyos_cli.plugins.builtin.documents.profiles.document_profile import (
    DocumentProfile,
)
from familyos_cli.plugins.builtin.documents.profiles.document_profile_registry import (
    DocumentProfileRegistry,
)


def create_profile(
    profile_id: str = "documents.profile.basic",
) -> DocumentProfile:
    """Create a test document profile."""

    return DocumentProfile(
        id=profile_id,
        name="Basic Documents Profile",
        version="1.0.0",
        level="BASIC",
        description="Basic document profile.",
    )


def test_registry_registers_profile() -> None:
    registry = DocumentProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.get(
        profile.id,
    ) == profile


def test_registry_returns_none_for_unknown_profile() -> None:
    registry = DocumentProfileRegistry()

    assert registry.get(
        "documents.profile.unknown",
    ) is None


def test_registry_lists_registered_profiles() -> None:
    registry = DocumentProfileRegistry()

    first = create_profile(
        "documents.profile.first",
    )
    second = create_profile(
        "documents.profile.second",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.list() == (
        first,
        second,
    )


def test_registry_replaces_profile_with_same_identifier() -> None:
    registry = DocumentProfileRegistry()

    first = create_profile()

    second = DocumentProfile(
        id="documents.profile.basic",
        name="Updated Documents Profile",
        version="2.0.0",
        level="STANDARD",
        description="Updated document profile.",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.get(
        "documents.profile.basic",
    ) == second