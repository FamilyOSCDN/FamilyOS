"""Tests for EducationValidator."""

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.validation.education_validator import (
    EducationValidator,
)


def test_standard_context_is_valid() -> None:
    """Standard education context should pass."""

    validator = EducationValidator()

    context = EducationContext(
        domain_name="family_learning",
        subject="student",
        required_level=EducationLevel.STANDARD,
    )

    result = validator.validate(
        context,
    )

    assert result.valid is True
    assert result.message == (
        "Education context validated."
    )


def test_critical_context_requires_review() -> None:
    """Critical context should fail validation."""

    validator = EducationValidator()

    context = EducationContext(
        domain_name="family_learning",
        subject="student",
        required_level=EducationLevel.CRITICAL,
    )

    result = validator.validate(
        context,
    )

    assert result.valid is False
    assert result.message == (
        "Critical education review required."
    )
