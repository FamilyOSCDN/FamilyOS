"""Subprocess-backed canonical validation gate."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.validation.ci_validation import (
    GateResult,
    ValidationStatus,
)

_MAX_DIAGNOSTIC_CHARACTERS = 2000


@dataclass(frozen=True, slots=True)
class SubprocessValidationGate:
    """Execute one explicit command without shell interpretation."""

    gate_id: str
    command: tuple[str, ...]
    cwd: Path

    def execute(self) -> GateResult:
        """Execute the command and normalize its validation result."""

        try:
            completed = subprocess.run(
                self.command,
                cwd=self.cwd,
                capture_output=True,
                check=False,
                text=True,
            )
        except Exception as error:  # noqa: BLE001 - execution boundary
            return GateResult(
                gate_id=self.gate_id,
                status=ValidationStatus.ERROR,
                diagnostic=self._normalize_diagnostic(str(error)),
            )

        if completed.returncode == 0:
            return GateResult(
                gate_id=self.gate_id,
                status=ValidationStatus.PASSED,
                exit_code=0,
            )

        diagnostic = completed.stderr.strip() or completed.stdout.strip()
        return GateResult(
            gate_id=self.gate_id,
            status=ValidationStatus.FAILED,
            exit_code=completed.returncode,
            diagnostic=self._normalize_diagnostic(diagnostic),
        )

    def _normalize_diagnostic(self, diagnostic: str) -> str:
        """Remove repository-specific paths and bound diagnostic size."""

        normalized = diagnostic.replace(str(self.cwd), ".").strip()
        if not normalized:
            return "Command failed without diagnostic output."
        return normalized[-_MAX_DIAGNOSTIC_CHARACTERS:]
