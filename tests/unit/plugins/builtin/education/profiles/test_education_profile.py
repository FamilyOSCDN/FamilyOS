"""Tests for EducationProfile."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.education.profiles.education_profile import (
    EducationProfile,
)


def test_education_profile_can_be_created() -> None:
    """Profile stores values."""

    profile = EducationProfile(
        id="education.profile.family",
        name="Family Education Profile",
        level="standard",
        description="Standard family education profile.",
    )

    assert profile.id == "education.profile.family"
    assert profile.name == "Family Education Profile"
    assert profile.level == "standard"
    assert profile.description == (
        "Standard family education profile."
    )


def test_education_profile_description_is_optional() -> None:
    """Description defaults to empty."""

    profile = EducationProfile(
        id="education.profile.basic",
        name="Basic Education Profile",
        level="basic",
    )

    assert profile.description == ""


def test_education_profile_is_immutable() -> None:
    """Profiles cannot be modified."""

    profile = EducationProfile(
        id="education.profile.basic",
        name="Basic Education Profile",
        level="basic",
    )

    with pytest.raises(FrozenInstanceError):
        profile.level = "critical"  # type: ignore[misc]
