"""Tests for FinanceProfile."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.finance.profiles.finance_profile import (
    FinanceProfile,
)


def test_finance_profile_can_be_created() -> None:
    """Finance profile stores values."""

    profile = FinanceProfile(
        id="finance.profile.family",
        name="Family Finance Profile",
        version="1.0.0",
        level="STANDARD",
        description="Finance profile for family environments.",
    )

    assert profile.id == "finance.profile.family"
    assert profile.name == "Family Finance Profile"
    assert profile.version == "1.0.0"
    assert profile.level == "STANDARD"
    assert profile.description == (
        "Finance profile for family environments."
    )


def test_finance_profile_description_is_optional() -> None:
    """Description defaults to empty."""

    profile = FinanceProfile(
        id="finance.profile.basic",
        name="Basic Finance Profile",
        version="1.0.0",
        level="BASIC",
    )

    assert profile.description == ""


def test_finance_profile_is_immutable() -> None:
    """Finance profiles cannot be modified."""

    profile = FinanceProfile(
        id="finance.profile.basic",
        name="Basic Finance Profile",
        version="1.0.0",
        level="BASIC",
    )

    with pytest.raises(FrozenInstanceError):
        profile.level = "CRITICAL"  # type: ignore[misc]
