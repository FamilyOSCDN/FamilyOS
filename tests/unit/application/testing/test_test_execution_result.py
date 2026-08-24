"""Tests for canonical Testing Framework execution-result models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.testing.test_execution_result import (
    TestExecutionResult as CanonicalExecutionResult,
)
from familyos_cli.application.testing.test_execution_result import (
    TestExecutionStatus as CanonicalExecutionStatus,
)
from familyos_cli.application.testing.test_execution_result import (
    TestExecutionSummary as CanonicalExecutionSummary,
)


def test_summary_preserves_canonical_execution_counts() -> None:
    summary = CanonicalExecutionSummary(
        discovered=12,
        executed=11,
        passed=8,
        failed=1,
        skipped=2,
        errors=0,
        duration_seconds=1.25,
    )

    assert summary.discovered == 12
    assert summary.executed == 11
    assert summary.passed == 8
    assert summary.failed == 1
    assert summary.skipped == 2
    assert summary.errors == 0
    assert summary.duration_seconds == pytest.approx(1.25)


def test_result_preserves_status_summary_and_diagnostic() -> None:
    summary = CanonicalExecutionSummary(
        discovered=3,
        executed=3,
        passed=2,
        failed=1,
        skipped=0,
        errors=0,
        duration_seconds=0.5,
    )

    result = CanonicalExecutionResult(
        status=CanonicalExecutionStatus.FAILED,
        summary=summary,
        diagnostic="one required test failed",
    )

    assert result.status is CanonicalExecutionStatus.FAILED
    assert result.summary is summary
    assert result.diagnostic == "one required test failed"


@pytest.mark.parametrize(
    "status, expected",
    (
        (CanonicalExecutionStatus.PASSED, True),
        (CanonicalExecutionStatus.FAILED, False),
        (CanonicalExecutionStatus.ERROR, False),
    ),
)
def test_successful_reflects_only_passed_status(
    status: CanonicalExecutionStatus,
    expected: bool,
) -> None:
    result = CanonicalExecutionResult(
        status=status,
        summary=CanonicalExecutionSummary(
            discovered=0,
            executed=0,
            passed=0,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=0.0,
        ),
    )

    assert result.successful is expected


@pytest.mark.parametrize(
    "field",
    (
        "discovered",
        "executed",
        "passed",
        "failed",
        "skipped",
        "errors",
    ),
)
def test_summary_rejects_negative_counts(field: str) -> None:
    values = {
        "discovered": 1,
        "executed": 1,
        "passed": 1,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
    }
    values[field] = -1

    with pytest.raises(ValueError, match="non-negative"):
        CanonicalExecutionSummary(
            **values,
            duration_seconds=0.0,
        )


def test_summary_rejects_negative_duration() -> None:
    with pytest.raises(
        ValueError,
        match="duration_seconds must be non-negative",
    ):
        CanonicalExecutionSummary(
            discovered=0,
            executed=0,
            passed=0,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=-0.1,
        )


def test_summary_rejects_executed_greater_than_discovered() -> None:
    with pytest.raises(
        ValueError,
        match="executed tests cannot exceed discovered tests",
    ):
        CanonicalExecutionSummary(
            discovered=2,
            executed=3,
            passed=3,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=0.1,
        )


def test_summary_rejects_outcome_total_greater_than_executed() -> None:
    with pytest.raises(
        ValueError,
        match="test outcome total cannot exceed executed tests",
    ):
        CanonicalExecutionSummary(
            discovered=3,
            executed=2,
            passed=2,
            failed=1,
            skipped=0,
            errors=0,
            duration_seconds=0.1,
        )


def test_models_are_immutable() -> None:
    summary = CanonicalExecutionSummary(
        discovered=1,
        executed=1,
        passed=1,
        failed=0,
        skipped=0,
        errors=0,
        duration_seconds=0.1,
    )
    result = CanonicalExecutionResult(
        status=CanonicalExecutionStatus.PASSED,
        summary=summary,
    )

    with pytest.raises(FrozenInstanceError):
        summary.passed = 0  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        result.status = CanonicalExecutionStatus.FAILED  # type: ignore[misc]
