"""Tests for EducationRule."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.education.rules.education_rule import (
    EducationRule,
)


def test_education_rule_can_be_created() -> None:
    """Rule stores values."""

    rule = EducationRule(
        id="education.rule.family",
        name="Family Learning Rule",
        level="standard",
        description="Standard learning rule.",
    )

    assert rule.id == "education.rule.family"
    assert rule.name == "Family Learning Rule"
    assert rule.level == "standard"
    assert rule.description == (
        "Standard learning rule."
    )


def test_education_rule_description_is_optional() -> None:
    """Description defaults to empty."""

    rule = EducationRule(
        id="education.rule.basic",
        name="Basic Learning Rule",
        level="basic",
    )

    assert rule.description == ""


def test_education_rule_is_immutable() -> None:
    """Rules cannot be modified."""

    rule = EducationRule(
        id="education.rule.basic",
        name="Basic Learning Rule",
        level="basic",
    )

    with pytest.raises(FrozenInstanceError):
        rule.level = "critical"  # type: ignore[misc]
