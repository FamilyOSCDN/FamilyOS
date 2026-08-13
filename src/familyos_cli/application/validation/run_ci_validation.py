"""Provider-neutral canonical CI validation runner."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.application.validation.ci_validation import (
    MANDATORY_CI_GATE_IDS,
    CiValidationResult,
    GateResult,
    ValidationStatus,
)


class ValidationGate(Protocol):
    """Execute one canonical validation gate."""

    @property
    def gate_id(self) -> str:
        """Return the stable gate identifier."""

    def execute(self) -> GateResult:
        """Execute the gate and return structured evidence."""


class RunCiValidationUseCase:
    """Run mandatory validation gates sequentially without fail-fast."""

    def __init__(self, gates: tuple[ValidationGate, ...]) -> None:
        """Initialize with the exact canonical gate sequence."""

        gate_ids = tuple(gate.gate_id for gate in gates)
        if gate_ids != MANDATORY_CI_GATE_IDS:
            raise ValueError(
                "CI validation gates must use canonical order: "
                f"{', '.join(MANDATORY_CI_GATE_IDS)}.",
            )
        self._gates = gates

    @property
    def gate_ids(self) -> tuple[str, ...]:
        """Return the configured canonical gate sequence."""

        return tuple(gate.gate_id for gate in self._gates)

    def execute(self) -> CiValidationResult:
        """Execute every gate and retain all results."""

        results: list[GateResult] = []
        for gate in self._gates:
            try:
                result = gate.execute()
            except Exception as error:  # noqa: BLE001 - gate execution boundary
                result = GateResult(
                    gate_id=gate.gate_id,
                    status=ValidationStatus.ERROR,
                    diagnostic=f"Unexpected gate execution error: {error}",
                )
            results.append(result)

        return CiValidationResult(gates=tuple(results))
