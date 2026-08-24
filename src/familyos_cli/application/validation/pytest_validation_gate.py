"""Testing Framework-backed canonical pytest validation gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.ports.testing import PytestRunnerPort
from familyos_cli.application.testing import (
    PytestResultNormalizer,
    TestExecutionStatus,
)
from familyos_cli.application.validation.ci_validation import (
    GateResult,
    ValidationStatus,
)


@dataclass(frozen=True, slots=True)
class PytestValidationGate:
    """Translate canonical Testing results into CI validation evidence."""

    runner: PytestRunnerPort
    normalizer: PytestResultNormalizer
    project_root: Path

    @property
    def gate_id(self) -> str:
        """Return the stable canonical pytest gate identifier."""

        return "pytest"

    def execute(self) -> GateResult:
        """Execute repository-wide pytest and return canonical gate evidence."""

        native_result = self.runner.run(
            project_root=self.project_root,
            test_paths=(),
        )

        canonical_result = self.normalizer.normalize(
            native_result,
        )

        status = {
            TestExecutionStatus.PASSED: ValidationStatus.PASSED,
            TestExecutionStatus.FAILED: ValidationStatus.FAILED,
            TestExecutionStatus.ERROR: ValidationStatus.ERROR,
        }[canonical_result.status]

        return GateResult(
            gate_id=self.gate_id,
            status=status,
            exit_code=native_result.exit_code,
            diagnostic=canonical_result.diagnostic,
        )
