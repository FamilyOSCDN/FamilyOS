"""Validate canonical build inputs before package execution."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.build_input_validation import (
    BuildInputValidationCheck,
    BuildInputValidationResult,
)
from familyos_cli.application.build.build_target_definition import (
    BuildTargetDefinition,
)


class BuildInputValidator:
    """Validate required inputs declared by a build target."""

    def validate(
        self,
        *,
        project_root: Path,
        target_definition: BuildTargetDefinition,
    ) -> BuildInputValidationResult:
        """Validate required target inputs."""

        checks = tuple(
            self._validate_input(
                project_root,
                input_name,
            )
            for input_name in target_definition.required_inputs
        )

        return BuildInputValidationResult(
            checks=checks,
        )

    def _validate_input(
        self,
        project_root: Path,
        input_name: str,
    ) -> BuildInputValidationCheck:
        if input_name == "package source governed by pyproject.toml":
            path = project_root / "src"
        else:
            path = project_root / input_name

        if path.exists():
            return BuildInputValidationCheck(
                input_name=input_name,
                successful=True,
            )

        return BuildInputValidationCheck(
            input_name=input_name,
            successful=False,
            diagnostic=(
                f"required build input missing: {input_name}"
            ),
        )
