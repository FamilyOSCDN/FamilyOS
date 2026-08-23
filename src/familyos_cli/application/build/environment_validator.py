"""Validate canonical observable build-environment invariants."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_validation import (
    EnvironmentValidationFinding,
    EnvironmentValidationResult,
    EnvironmentValidationStatus,
)


class EnvironmentValidator:
    """Validate observable invariants required for canonical build execution."""

    def validate(
        self,
        *,
        state: EnvironmentState,
    ) -> EnvironmentValidationResult:
        """Validate deterministic environment invariants."""

        findings: list[EnvironmentValidationFinding] = []

        self._validate_temporary_directory(
            state=state,
            findings=findings,
        )

        if findings:
            return EnvironmentValidationResult(
                status=EnvironmentValidationStatus.FAILED,
                findings=tuple(findings),
            )

        return EnvironmentValidationResult(
            status=EnvironmentValidationStatus.SUCCEEDED,
        )

    @staticmethod
    def _validate_temporary_directory(
        *,
        state: EnvironmentState,
        findings: list[EnvironmentValidationFinding],
    ) -> None:
        temporary_directory = Path(state.temporary_directory)

        if temporary_directory.is_dir():
            return

        findings.append(
            EnvironmentValidationFinding(
                component="temporary-storage",
                diagnostic=(
                    "temporary directory is unavailable: "
                    f"{state.temporary_directory}"
                ),
            )
        )
