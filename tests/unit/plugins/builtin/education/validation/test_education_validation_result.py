"""Tests for EducationValidationResult."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.education.validation.education_validation_result import (
    EducationValidationResult,
)


def test_validation_result_can_be_created() -> None:
    """Validation result stores values."""

    result = EducationValidationResult(
        valid=True,
        message="Education validated.",
    )

    assert result.valid is True
    assert result.message == (
        "Education validated."
    )


def test_validation_result_message_is_optional() -> None:
    """Message defaults to empty."""

    result = EducationValidationResult(
        valid=False,
    )

    assert result.message == ""


def test_validation_result_is_immutable() -> None:
    """Validation results cannot be modified."""

    result = EducationValidationResult(
        valid=True,
    )

    with pytest.raises(FrozenInstanceError):
        result.valid = False  # type: ignore[misc]
