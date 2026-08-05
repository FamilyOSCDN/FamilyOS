"""Tests for EducationPolicy."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.education.policies.education_policy import (
    EducationPolicy,
)


def test_education_policy_can_be_created() -> None:
    """Policy stores values."""

    policy = EducationPolicy(
        id="education.policy.family",
        name="Family Education Policy",
        level="standard",
        description="Standard family education policy.",
    )

    assert policy.id == "education.policy.family"
    assert policy.name == "Family Education Policy"
    assert policy.level == "standard"
    assert policy.description == (
        "Standard family education policy."
    )


def test_education_policy_description_is_optional() -> None:
    """Description defaults to empty."""

    policy = EducationPolicy(
        id="education.policy.basic",
        name="Basic Education Policy",
        level="basic",
    )

    assert policy.description == ""


def test_education_policy_is_immutable() -> None:
    """Policies cannot be modified."""

    policy = EducationPolicy(
        id="education.policy.basic",
        name="Basic Education Policy",
        level="basic",
    )

    with pytest.raises(FrozenInstanceError):
        policy.level = "critical"  # type: ignore[misc]
