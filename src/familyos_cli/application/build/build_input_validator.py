"""Validate canonical build inputs before package execution."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from familyos_cli.application.build.build_input_validation import (
    BuildInputValidationCheck,
    BuildInputValidationResult,
)
from familyos_cli.application.build.build_target_definition import (
    BuildTargetDefinition,
)
from familyos_cli.application.build.dependency_input_freshness import (
    validate_dependency_input_freshness,
)


class BuildInputValidator:
    """Validate required inputs declared by a build target."""

    def validate(
        self,
        *,
        project_root: Path,
        target_definition: BuildTargetDefinition,
    ) -> BuildInputValidationResult:
        """Validate canonical target inputs before transformation."""

        checks = tuple(
            self._validate_input(
                project_root,
                input_name,
            )
            for input_name in target_definition.required_inputs
        )

        if not all(check.successful for check in checks):
            return BuildInputValidationResult(
                checks=checks,
            )

        metadata_check = self._validate_package_metadata(
            project_root,
        )
        checks = (*checks, metadata_check)

        if not metadata_check.successful:
            return BuildInputValidationResult(
                checks=checks,
            )

        freshness_check = self._validate_generated_dependency_input(
            project_root,
        )

        return BuildInputValidationResult(
            checks=(*checks, freshness_check),
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
            diagnostic=f"required build input missing: {input_name}",
        )

    def _validate_package_metadata(
        self,
        project_root: Path,
    ) -> BuildInputValidationCheck:
        input_name = "package metadata"
        pyproject_path = project_root / "pyproject.toml"

        try:
            with pyproject_path.open("rb") as pyproject_file:
                document = tomllib.load(pyproject_file)
        except (OSError, tomllib.TOMLDecodeError):
            return BuildInputValidationCheck(
                input_name=input_name,
                successful=False,
                diagnostic="build metadata pyproject.toml is malformed",
            )

        project = document.get("project")
        if not isinstance(project, dict):
            return BuildInputValidationCheck(
                input_name=input_name,
                successful=False,
                diagnostic=(
                    "build metadata pyproject.toml does not contain "
                    "a valid [project] table"
                ),
            )

        for field_name in (
            "name",
            "version",
            "requires-python",
        ):
            if not self._is_non_empty_string(
                project.get(field_name),
            ):
                return BuildInputValidationCheck(
                    input_name=input_name,
                    successful=False,
                    diagnostic=(
                        "build metadata pyproject.toml project."
                        f"{field_name} is missing or invalid"
                    ),
                )

        return BuildInputValidationCheck(
            input_name=input_name,
            successful=True,
        )

    def _validate_generated_dependency_input(
        self,
        project_root: Path,
    ) -> BuildInputValidationCheck:
        input_name = "generated dependency input freshness"

        result = validate_dependency_input_freshness(
            pyproject_path=project_root / "pyproject.toml",
            requirements_path=project_root / "requirements.txt",
        )

        return BuildInputValidationCheck(
            input_name=input_name,
            successful=result.successful,
            diagnostic=result.diagnostic,
        )

    @staticmethod
    def _is_non_empty_string(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())
