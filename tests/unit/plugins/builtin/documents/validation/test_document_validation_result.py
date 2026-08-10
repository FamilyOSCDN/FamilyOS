"""Tests for DocumentValidationResult."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.documents.validation.document_validation_result import (
    DocumentValidationResult,
)


def test_validation_result_can_be_created() -> None:
    """Validation result stores values."""

    result = DocumentValidationResult(
        valid=True,
        message="Validation successful.",
    )

    assert result.valid is True
    assert result.message == (
        "Validation successful."
    )


def test_validation_result_message_is_optional() -> None:
    """Message defaults to empty."""

    result = DocumentValidationResult(
        valid=False,
    )

    assert result.message == ""


def test_validation_result_is_immutable() -> None:
    """Validation results cannot be modified."""

    result = DocumentValidationResult(
        valid=True,
    )

    with pytest.raises(FrozenInstanceError):
        result.valid = False  # type: ignore[misc]