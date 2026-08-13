"""Tests for SecurityProfile."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.security.profiles.security_profile import (
    SecurityProfile,
)


def create_profile(
    **overrides: str,
) -> SecurityProfile:
    """Create a security profile for tests."""

    values = {
        "id": "security.profile.basic",
        "name": "Basic Security Profile",
        "version": "1.0.0",
        "level": "BASIC",
        "description": "",
    }
    values.update(
        overrides,
    )

    return SecurityProfile(
        id=values["id"],
        name=values["name"],
        version=values["version"],
        level=values["level"],
        description=values["description"],
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
    profile = create_profile()

    assert profile.description == ""


def test_security_profile_is_immutable() -> None:
    profile = create_profile()

    with pytest.raises(FrozenInstanceError):
        profile.level = "ENTERPRISE"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "message"),
    [
        (
            "id",
            "Security profile id cannot be empty.",
        ),
        (
            "name",
            "Security profile name cannot be empty.",
        ),
        (
            "version",
            "Security profile version cannot be empty.",
        ),
        (
            "level",
            "Security profile level cannot be empty.",
        ),
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "   ",
    ],
)
def test_security_profile_rejects_empty_required_fields(
    field: str,
    message: str,
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=message,
    ):
        create_profile(
            **{
                field: invalid_value,
            },
        )
