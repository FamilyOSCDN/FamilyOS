"""Testing Evidence-backed canonical pytest validation gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.ports.testing.testing_execution import (
    TestingExecutionPort,
)
from familyos_cli.application.testing.test_execution_result import (
    TestExecutionStatus,
)
from familyos_cli.application.validation.ci_validation import (
    GateResult,
    ValidationStatus,
)


@dataclass(frozen=True, slots=True)
class PytestValidationGate:
    """Translate canonical Testing Evidence into CI validation evidence."""

    execution: TestingExecutionPort
    project_root: Path

    @property
    def gate_id(self) -> str:
        """Return the stable canonical pytest gate identifier."""

        return "pytest"

    def execute(self) -> GateResult:
        """Execute canonical Testing and translate its evidence."""

        evidence = self.execution.execute(
            project_root=self.project_root,
            test_paths=(),
        )

        canonical_result = evidence.result

        status = {
            TestExecutionStatus.PASSED: ValidationStatus.PASSED,
            TestExecutionStatus.FAILED: ValidationStatus.FAILED,
            TestExecutionStatus.ERROR: ValidationStatus.ERROR,
        }[canonical_result.status]

        return GateResult(
            gate_id=self.gate_id,
            status=status,
            exit_code=evidence.native_exit_code,
            diagnostic=canonical_result.diagnostic,
            testing_evidence=evidence,
        )
