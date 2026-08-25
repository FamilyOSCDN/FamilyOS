"""Tests for the Testing Evidence-backed canonical pytest validation gate."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from familyos_cli.application.ports.testing import TestingExecutionPort
from familyos_cli.application.testing import (
    TestExecutionId as CanonicalExecutionId,
)
from familyos_cli.application.testing import (
    TestExecutionResult as CanonicalExecutionResult,
)
from familyos_cli.application.testing import (
    TestExecutionStatus as CanonicalExecutionStatus,
)
from familyos_cli.application.testing import (
    TestExecutionSummary as CanonicalExecutionSummary,
)
from familyos_cli.application.testing import (
    TestingEvidence as CanonicalTestingEvidence,
)
from familyos_cli.application.validation import ValidationStatus
from familyos_cli.application.validation.pytest_validation_gate import (
    PytestValidationGate,
)


class _RecordingTestingExecution(TestingExecutionPort):
    def __init__(
        self,
        evidence: CanonicalTestingEvidence,
    ) -> None:
        self.evidence = evidence
        self.calls: list[tuple[Path, tuple[Path, ...]]] = []

    def execute(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> CanonicalTestingEvidence:
        self.calls.append((project_root, test_paths))
        return self.evidence


def _evidence(
    *,
    status: CanonicalExecutionStatus,
    native_exit_code: int,
    passed: int = 0,
    failed: int = 0,
    errors: int = 0,
    diagnostic: str | None = None,
) -> CanonicalTestingEvidence:
    executed = passed + failed + errors

    return CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        result=CanonicalExecutionResult(
            status=status,
            summary=CanonicalExecutionSummary(
                discovered=executed,
                executed=executed,
                passed=passed,
                failed=failed,
                skipped=0,
                errors=errors,
                duration_seconds=0.1,
            ),
            diagnostic=diagnostic,
        ),
        captured_at=datetime(
            2026,
            8,
            25,
            7,
            45,
            tzinfo=UTC,
        ),
        native_exit_code=native_exit_code,
    )


def test_gate_has_canonical_pytest_identifier(
    tmp_path: Path,
) -> None:
    execution = _RecordingTestingExecution(
        _evidence(
            status=CanonicalExecutionStatus.PASSED,
            native_exit_code=0,
            passed=1,
        )
    )

    gate = PytestValidationGate(
        execution=execution,
        project_root=tmp_path,
    )

    assert gate.gate_id == "pytest"


def test_passing_test_execution_produces_passing_gate(
    tmp_path: Path,
) -> None:
    result = PytestValidationGate(
        execution=_RecordingTestingExecution(
            _evidence(
                status=CanonicalExecutionStatus.PASSED,
                native_exit_code=0,
                passed=3,
            )
        ),
        project_root=tmp_path,
    ).execute()

    assert result.gate_id == "pytest"
    assert result.status is ValidationStatus.PASSED
    assert result.exit_code == 0
    assert result.diagnostic is None


def test_failed_test_execution_produces_failed_gate(
    tmp_path: Path,
) -> None:
    result = PytestValidationGate(
        execution=_RecordingTestingExecution(
            _evidence(
                status=CanonicalExecutionStatus.FAILED,
                native_exit_code=1,
                failed=1,
                diagnostic="one test failed",
            )
        ),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.FAILED
    assert result.exit_code == 1
    assert result.diagnostic == "one test failed"


def test_pytest_execution_error_produces_error_gate(
    tmp_path: Path,
) -> None:
    result = PytestValidationGate(
        execution=_RecordingTestingExecution(
            _evidence(
                status=CanonicalExecutionStatus.ERROR,
                native_exit_code=2,
                errors=1,
                diagnostic="pytest execution error",
            )
        ),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.exit_code == 2
    assert result.diagnostic == "pytest execution error"


def test_gate_preserves_repository_wide_pytest_selection(
    tmp_path: Path,
) -> None:
    execution = _RecordingTestingExecution(
        _evidence(
            status=CanonicalExecutionStatus.PASSED,
            native_exit_code=0,
            passed=1,
        )
    )

    PytestValidationGate(
        execution=execution,
        project_root=tmp_path,
    ).execute()

    assert execution.calls == [
        (
            tmp_path,
            (),
        )
    ]
