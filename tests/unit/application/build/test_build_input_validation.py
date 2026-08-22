"""Tests for canonical build input validation models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.build.build_input_validation import (
    BuildInputValidationCheck,
    BuildInputValidationResult,
)


def test_validation_result_is_successful_when_all_checks_pass() -> None:
    result = BuildInputValidationResult(
        checks=(
            BuildInputValidationCheck(
                input_name="pyproject.toml",
                successful=True,
            ),
            BuildInputValidationCheck(
                input_name="requirements.txt",
                successful=True,
            ),
        ),
    )

    assert result.successful is True
    assert result.diagnostic is None


def test_validation_result_is_failed_when_one_check_fails() -> None:
    result = BuildInputValidationResult(
        checks=(
            BuildInputValidationCheck(
                input_name="pyproject.toml",
                successful=True,
            ),
            BuildInputValidationCheck(
                input_name="requirements.txt",
                successful=False,
                diagnostic="missing requirements.txt",
            ),
        ),
    )

    assert result.successful is False
    assert result.diagnostic == "missing requirements.txt"


def test_validation_check_is_immutable() -> None:
    check = BuildInputValidationCheck(
        input_name="pyproject.toml",
        successful=True,
    )

    with pytest.raises(FrozenInstanceError):
        check.successful = False  # type: ignore[misc]


def test_validation_result_is_immutable() -> None:
    result = BuildInputValidationResult(
        checks=(),
    )

    with pytest.raises(FrozenInstanceError):
        result.checks = ()  # type: ignore[misc]
