"""Tests for the Testing Framework-backed canonical pytest validation gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.ports.testing import PytestRunnerPort
from familyos_cli.application.testing import (
    PytestExecutionResult,
    PytestResultNormalizer,
)
from familyos_cli.application.validation import ValidationStatus
from familyos_cli.application.validation.pytest_validation_gate import (
    PytestValidationGate,
)


@dataclass
class _RecordingPytestRunner(PytestRunnerPort):
    result: PytestExecutionResult

    def __post_init__(self) -> None:
        self.calls: list[tuple[Path, tuple[Path, ...]]] = []

    def run(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> PytestExecutionResult:
        self.calls.append((project_root, test_paths))
        return self.result


def _native_result(
    *,
    exit_code: int,
    passed: int = 0,
    failed: int = 0,
    errors: int = 0,
    diagnostic: str | None = None,
) -> PytestExecutionResult:
    executed = passed + failed + errors

    return PytestExecutionResult(
        exit_code=exit_code,
        discovered=executed,
        executed=executed,
        passed=passed,
        failed=failed,
        skipped=0,
        errors=errors,
        duration_seconds=0.1,
        diagnostic=diagnostic,
    )


def test_gate_has_canonical_pytest_identifier(
    tmp_path: Path,
) -> None:
    runner = _RecordingPytestRunner(
        _native_result(exit_code=0, passed=1)
    )

    gate = PytestValidationGate(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        project_root=tmp_path,
    )

    assert gate.gate_id == "pytest"


def test_passing_test_execution_produces_passing_gate(
    tmp_path: Path,
) -> None:
    runner = _RecordingPytestRunner(
        _native_result(exit_code=0, passed=3)
    )

    result = PytestValidationGate(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        project_root=tmp_path,
    ).execute()

    assert result.gate_id == "pytest"
    assert result.status is ValidationStatus.PASSED
    assert result.exit_code == 0
    assert result.diagnostic is None


def test_failed_test_execution_produces_failed_gate(
    tmp_path: Path,
) -> None:
    runner = _RecordingPytestRunner(
        _native_result(
            exit_code=1,
            failed=1,
            diagnostic="one test failed",
        )
    )

    result = PytestValidationGate(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.FAILED
    assert result.exit_code == 1
    assert result.diagnostic == "one test failed"


def test_pytest_execution_error_produces_error_gate(
    tmp_path: Path,
) -> None:
    runner = _RecordingPytestRunner(
        _native_result(
            exit_code=2,
            errors=1,
            diagnostic="pytest execution error",
        )
    )

    result = PytestValidationGate(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.exit_code == 2
    assert result.diagnostic == "pytest execution error"


def test_gate_preserves_repository_wide_pytest_selection(
    tmp_path: Path,
) -> None:
    runner = _RecordingPytestRunner(
        _native_result(exit_code=0, passed=1)
    )

    PytestValidationGate(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        project_root=tmp_path,
    ).execute()

    assert runner.calls == [
        (
            tmp_path,
            (),
        )
    ]
