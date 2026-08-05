"""Tests for EducationProfileResolver."""

from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.profiles.education_profile import (
    EducationProfile,
)
from familyos_cli.plugins.builtin.education.profiles.education_profile_resolver import (
    EducationProfileResolver,
)


def test_resolver_returns_basic_level() -> None:
    """Resolver returns BASIC level."""

    resolver = EducationProfileResolver()

    profile = EducationProfile(
        id="education.profile.basic",
        name="Basic Education Profile",
        level="basic",
    )

    assert resolver.resolve(
        profile,
    ) == EducationLevel.BASIC


def test_resolver_returns_critical_level() -> None:
    """Resolver returns CRITICAL level."""

    resolver = EducationProfileResolver()

    profile = EducationProfile(
        id="education.profile.critical",
        name="Critical Education Profile",
        level="critical",
    )

    assert resolver.resolve(
        profile,
    ) == EducationLevel.CRITICAL
