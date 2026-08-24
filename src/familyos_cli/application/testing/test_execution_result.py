"""Canonical Testing Framework execution-result models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TestExecutionStatus(StrEnum):
    """Aggregate outcome of one canonical test execution."""

    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class TestExecutionSummary:
    """Canonical aggregate summary of one test execution."""

    discovered: int
    executed: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration_seconds: float

    def __post_init__(self) -> None:
        """Reject inconsistent canonical test-execution summaries."""

        counts = (
            self.discovered,
            self.executed,
            self.passed,
            self.failed,
            self.skipped,
            self.errors,
        )

        if any(value < 0 for value in counts):
            raise ValueError("test execution counts must be non-negative")

        if self.duration_seconds < 0:
            raise ValueError(
                "duration_seconds must be non-negative"
            )

        if self.executed > self.discovered:
            raise ValueError(
                "executed tests cannot exceed discovered tests"
            )

        outcome_total = (
            self.passed
            + self.failed
            + self.skipped
            + self.errors
        )

        if outcome_total > self.executed:
            raise ValueError(
                "test outcome total cannot exceed executed tests"
            )


@dataclass(frozen=True, slots=True)
class TestExecutionResult:
    """Runner-independent canonical result of one test execution."""

    status: TestExecutionStatus
    summary: TestExecutionSummary
    diagnostic: str | None = None

    @property
    def successful(self) -> bool:
        """Return whether the canonical test execution passed."""

        return self.status is TestExecutionStatus.PASSED
