"""Tests for canonical CI validation aggregation."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from familyos_cli.application.validation import (
    MANDATORY_CI_GATE_IDS,
    GateResult,
    RunCiValidationUseCase,
    ValidationStatus,
)


@dataclass
class _Gate:
    gate_id: str
    status: ValidationStatus
    calls: list[str]

    def execute(self) -> GateResult:
        self.calls.append(self.gate_id)
        return GateResult(gate_id=self.gate_id, status=self.status)


@dataclass
class _ExplodingGate:
    gate_id: str
    calls: list[str]

    def execute(self) -> GateResult:
        self.calls.append(self.gate_id)
        raise RuntimeError("adapter crashed")


def _runner(
    statuses: tuple[ValidationStatus, ...],
    calls: list[str],
) -> RunCiValidationUseCase:
    return RunCiValidationUseCase(
        tuple(
            _Gate(gate_id, status, calls)
            for gate_id, status in zip(MANDATORY_CI_GATE_IDS, statuses, strict=True)
        ),
    )


def test_all_gates_pass_in_canonical_order() -> None:
    calls: list[str] = []
    runner = _runner((ValidationStatus.PASSED,) * 6, calls)

    result = runner.execute()

    assert result.status is ValidationStatus.PASSED
    assert calls == list(MANDATORY_CI_GATE_IDS)
    assert tuple(gate.gate_id for gate in result.gates) == MANDATORY_CI_GATE_IDS


@pytest.mark.parametrize(
    "statuses",
    (
        (
            ValidationStatus.PASSED,
            ValidationStatus.FAILED,
            ValidationStatus.PASSED,
            ValidationStatus.PASSED,
            ValidationStatus.PASSED,
            ValidationStatus.PASSED,
        ),
        (
            ValidationStatus.FAILED,
            ValidationStatus.PASSED,
            ValidationStatus.FAILED,
            ValidationStatus.PASSED,
            ValidationStatus.PASSED,
            ValidationStatus.PASSED,
        ),
    ),
)
def test_one_or_multiple_failures_produce_failed_result(
    statuses: tuple[ValidationStatus, ...],
) -> None:
    calls: list[str] = []
    result = _runner(statuses, calls).execute()

    assert result.status is ValidationStatus.FAILED
    assert calls == list(MANDATORY_CI_GATE_IDS)


def test_error_takes_precedence_and_execution_continues() -> None:
    calls: list[str] = []
    statuses = (
        ValidationStatus.FAILED,
        ValidationStatus.ERROR,
        ValidationStatus.PASSED,
        ValidationStatus.PASSED,
        ValidationStatus.PASSED,
        ValidationStatus.PASSED,
    )

    result = _runner(statuses, calls).execute()

    assert result.status is ValidationStatus.ERROR
    assert calls == list(MANDATORY_CI_GATE_IDS)


def test_unexpected_gate_exception_becomes_error_and_execution_continues() -> None:
    calls: list[str] = []
    gates = tuple(
        _ExplodingGate(gate_id, calls)
        if gate_id == "ruff"
        else _Gate(gate_id, ValidationStatus.PASSED, calls)
        for gate_id in MANDATORY_CI_GATE_IDS
    )

    result = RunCiValidationUseCase(gates).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.gates[2].diagnostic == (
        "Unexpected gate execution error: adapter crashed"
    )
    assert calls == list(MANDATORY_CI_GATE_IDS)


def test_runner_rejects_noncanonical_gate_order() -> None:
    calls: list[str] = []
    gates = tuple(
        _Gate(gate_id, ValidationStatus.PASSED, calls)
        for gate_id in reversed(MANDATORY_CI_GATE_IDS)
    )

    with pytest.raises(ValueError, match="canonical order"):
        RunCiValidationUseCase(gates)
