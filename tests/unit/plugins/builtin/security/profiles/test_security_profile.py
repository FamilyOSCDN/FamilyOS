from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.security.profiles.security_profile import (
    SecurityProfile,
)


def test_security_profile_can_be_created() -> None:
    profile = SecurityProfile(
        id="security.profile.family",
        name="Family Security Profile",
        version="1.0.0",
        level="FAMILY",
        description="Security profile for family environments.",
    )

    assert profile.id == "security.profile.family"
    assert profile.name == "Family Security Profile"
    assert profile.version == "1.0.0"
    assert profile.level == "FAMILY"
    assert profile.description == (
        "Security profile for family environments."
    )


def test_security_profile_description_is_optional() -> None:
    profile = SecurityProfile(
        id="security.profile.basic",
        name="Basic Security Profile",
        version="1.0.0",
        level="BASIC",
    )

    assert profile.description == ""


def test_security_profile_is_immutable() -> None:
    profile = SecurityProfile(
        id="security.profile.basic",
        name="Basic Security Profile",
        version="1.0.0",
        level="BASIC",
    )

    with pytest.raises(FrozenInstanceError):
        profile.level = "ENTERPRISE"  # type: ignore[misc]
