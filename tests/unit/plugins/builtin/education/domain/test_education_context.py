"""Tests for EducationContext."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)


def test_education_context_can_be_created() -> None:
    """Context stores education information."""

    context = EducationContext(
        domain_name="family_learning",
        subject="student",
        required_level=EducationLevel.STANDARD,
    )

    assert context.domain_name == "family_learning"
    assert context.subject == "student"
    assert (
        context.required_level
        == EducationLevel.STANDARD
    )


def test_education_context_is_immutable() -> None:
    """Context cannot be modified."""

    context = EducationContext(
        domain_name="family_learning",
        subject="student",
        required_level=EducationLevel.BASIC,
    )

    with pytest.raises(FrozenInstanceError):
        context.subject = "teacher"  # type: ignore[misc]
