"""Tests for EducationProfileRegistry."""

import pytest

from familyos_cli.plugins.builtin.education.profiles.education_profile import (
    EducationProfile,
)
from familyos_cli.plugins.builtin.education.profiles.education_profile_registry import (
    EducationProfileRegistry,
)


def create_profile(
    profile_id: str = "education.profile.basic",
) -> EducationProfile:
    """Create test profile."""

    return EducationProfile(
        id=profile_id,
        name="Basic Education Profile",
        level="basic",
    )


def test_registry_registers_profile() -> None:
    """Registered profiles should be retrievable."""

    registry = EducationProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.get(
        profile.id,
    ) == profile


def test_registry_returns_none_for_unknown_profile() -> None:
    """Unknown profile identifiers should return none."""

    registry = EducationProfileRegistry()

    assert registry.get(
        "education.profile.unknown",
    ) is None


def test_registry_lists_profiles() -> None:
    """Profiles should be listed in registration order."""

    registry = EducationProfileRegistry()

    first = create_profile(
        "education.profile.first",
    )
    second = create_profile(
        "education.profile.second",
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


def test_registry_rejects_duplicate_profile_id() -> None:
    """Duplicate profile identifiers should be rejected."""

    registry = EducationProfileRegistry()

    first = create_profile()
    duplicate = EducationProfile(
        id=first.id,
        name="Replacement Profile",
        level="critical",
    )

    registry.register(
        first,
    )

    with pytest.raises(
        ValueError,
        match=(
            "Education profile "
            "'education.profile.basic' "
            "is already registered."
        ),
    ):
        registry.register(
            duplicate,
        )

    assert registry.get(
        first.id,
    ) == first

    assert registry.list() == (
        first,
    )
