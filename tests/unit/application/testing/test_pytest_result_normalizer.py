"""Tests for canonical normalization of structured pytest results."""

from __future__ import annotations

import pytest
from familyos_cli.application.testing.pytest_result_normalizer import (
    PytestExecutionResult,
    PytestResultNormalizer,
)

from familyos_cli.application.testing.test_execution_result import (
    TestExecutionStatus as CanonicalExecutionStatus,
)


def test_normalizer_maps_successful_pytest_execution() -> None:
    native = PytestExecutionResult(
        exit_code=0,
        discovered=12,
        executed=11,
        passed=8,
        failed=0,
        skipped=3,
        errors=0,
        duration_seconds=1.25,
    )

    result = PytestResultNormalizer().normalize(native)

    assert result.status is CanonicalExecutionStatus.PASSED
    assert result.summary.discovered == 12
    assert result.summary.executed == 11
    assert result.summary.passed == 8
    assert result.summary.failed == 0
    assert result.summary.skipped == 3
    assert result.summary.errors == 0
    assert result.summary.duration_seconds == 1.25
    assert result.diagnostic is None


def test_normalizer_maps_test_failure() -> None:
    native = PytestExecutionResult(
        exit_code=1,
        discovered=4,
        executed=4,
        passed=3,
        failed=1,
        skipped=0,
        errors=0,
        duration_seconds=0.5,
        diagnostic="one test failed",
    )

    result = PytestResultNormalizer().normalize(native)

    assert result.status is CanonicalExecutionStatus.FAILED
    assert result.summary.failed == 1
    assert result.summary.errors == 0
    assert result.diagnostic == "one test failed"


def test_normalizer_maps_execution_error() -> None:
    native = PytestExecutionResult(
        exit_code=2,
        discovered=2,
        executed=1,
        passed=0,
        failed=0,
        skipped=0,
        errors=1,
        duration_seconds=0.25,
        diagnostic="pytest execution error",
    )

    result = PytestResultNormalizer().normalize(native)

    assert result.status is CanonicalExecutionStatus.ERROR
    assert result.summary.errors == 1
    assert result.diagnostic == "pytest execution error"


def test_native_result_rejects_negative_exit_code() -> None:
    with pytest.raises(
        ValueError,
        match="pytest exit code must be non-negative",
    ):
        PytestExecutionResult(
            exit_code=-1,
            discovered=0,
            executed=0,
            passed=0,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=0.0,
        )


def test_unknown_nonzero_exit_code_normalizes_to_error() -> None:
    native = PytestExecutionResult(
        exit_code=99,
        discovered=0,
        executed=0,
        passed=0,
        failed=0,
        skipped=0,
        errors=0,
        duration_seconds=0.0,
        diagnostic="unexpected pytest termination",
    )

    result = PytestResultNormalizer().normalize(native)

    assert result.status is CanonicalExecutionStatus.ERROR
    assert result.diagnostic == "unexpected pytest termination"
