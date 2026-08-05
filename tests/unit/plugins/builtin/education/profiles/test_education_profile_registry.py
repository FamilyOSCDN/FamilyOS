"""Tests for EducationProfileRegistry."""

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
    registry = EducationProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.get(
        profile.id,
    ) == profile


def test_registry_returns_none_for_unknown_profile() -> None:
    registry = EducationProfileRegistry()

    assert registry.get(
        "education.profile.unknown",
    ) is None


def test_registry_lists_profiles() -> None:
    registry = EducationProfileRegistry()

    first = create_profile(
        "education.profile.first",
    )
    second = create_profile(
        "education.profile.second",
    )

    registry.register(first)
    registry.register(second)

    assert registry.list() == (
        first,
        second,
    )
