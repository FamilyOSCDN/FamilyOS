"""Normalize structured pytest execution results into canonical test results."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.testing.test_execution_result import (
    TestExecutionResult,
    TestExecutionStatus,
    TestExecutionSummary,
)


@dataclass(frozen=True, slots=True)
class PytestExecutionResult:
    """Structured runner-specific outcome of one pytest execution."""

    exit_code: int
    discovered: int
    executed: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration_seconds: float
    diagnostic: str | None = None

    def __post_init__(self) -> None:
        """Reject invalid structured pytest execution state."""

        if self.exit_code < 0:
            raise ValueError("pytest exit code must be non-negative")

        # Reuse the canonical summary invariants at the runner boundary.
        TestExecutionSummary(
            discovered=self.discovered,
            executed=self.executed,
            passed=self.passed,
            failed=self.failed,
            skipped=self.skipped,
            errors=self.errors,
            duration_seconds=self.duration_seconds,
        )


class PytestResultNormalizer:
    """Translate structured pytest outcomes into canonical Testing results."""

    def normalize(
        self,
        result: PytestExecutionResult,
    ) -> TestExecutionResult:
        """Return the runner-independent canonical test execution result."""

        summary = TestExecutionSummary(
            discovered=result.discovered,
            executed=result.executed,
            passed=result.passed,
            failed=result.failed,
            skipped=result.skipped,
            errors=result.errors,
            duration_seconds=result.duration_seconds,
        )

        if result.exit_code == 0:
            status = TestExecutionStatus.PASSED
        elif result.exit_code == 1:
            status = TestExecutionStatus.FAILED
        else:
            status = TestExecutionStatus.ERROR

        return TestExecutionResult(
            status=status,
            summary=summary,
            diagnostic=result.diagnostic,
        )
