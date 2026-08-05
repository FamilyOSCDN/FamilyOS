"""Tests for FinanceValidationResult."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.finance.validation.finance_validation_result import (
    FinanceValidationResult,
)


def test_validation_result_can_be_created() -> None:
    """Validation result stores values."""

    result = FinanceValidationResult(
        valid=True,
        message="Validation successful.",
    )

    assert result.valid is True
    assert result.message == (
        "Validation successful."
    )


def test_validation_result_message_is_optional() -> None:
    """Message defaults to empty."""

    result = FinanceValidationResult(
        valid=False,
    )

    assert result.message == ""


def test_validation_result_is_immutable() -> None:
    """Validation results cannot be modified."""

    result = FinanceValidationResult(
        valid=True,
    )

    with pytest.raises(FrozenInstanceError):
        result.valid = False  # type: ignore[misc]
