"""Canonical FamilyOS package-build command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.application.build import (
    BuildEvidenceFactory,
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationRequirement,
)
from familyos_cli.application.build.build_validation_checks import (
    BuildValidationCheckFactory,
)
from familyos_cli.application.build.build_validation_orchestrator import (
    BuildValidationOrchestrator,
)
from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.rendering.build_evidence_json import (
    BuildEvidenceJsonRenderer,
)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
DEFAULT_OUTPUT_DIR = Path("dist")


def run_package_build(
    output_dir: Path,
    *,
    functional_validation: bool,
    evidence_output: Path | None = None,
) -> int:
    """Execute and render the canonical package build."""

    result = CommandContext().run_package_build.execute(
        output_dir,
        validate_functionally=functional_validation,
    )

    _render_result(result)

    if not result.successful:
        return EXIT_FAILURE

    if evidence_output is not None:
        functional_requirement = (
            BuildValidationRequirement.REQUIRED
            if functional_validation
            else BuildValidationRequirement.OPTIONAL
        )

        checks = BuildValidationCheckFactory().from_package_build(
            result,
            functional_requirement=functional_requirement,
        )

        validation_result = BuildValidationOrchestrator().execute(
            build_id=result.build_id,
            profile=BuildValidationProfile.CI,
            checks=checks,
        )

        evidence = BuildEvidenceFactory().from_package_build(
            result,
            validation_result,
        )

        rendered = BuildEvidenceJsonRenderer().render(evidence)

        evidence_output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        evidence_output.write_text(
            rendered,
            encoding="utf-8",
        )

    return EXIT_SUCCESS


def _render_result(result: CanonicalPackageBuildResult) -> None:
    """Render process-level build output without trust claims."""

    typer.echo(f"Canonical Package Build: {result.status.value.upper()}")
    typer.echo(f"Build ID: {result.build_id}")

    if result.build_context is not None:
        context = result.build_context
        typer.echo(f"Build Profile: {context.profile.value}")
        typer.echo(f"Build Target: {context.target.value}")
        typer.echo(f"Runtime Version: {context.runtime_version}")
        for component in context.toolchain_state.critical_versions:
            typer.echo(
                f"Toolchain {component.distribution}: {component.version}"
            )
        typer.echo(f"Output Directory: {context.output_dir}")
        typer.echo(
            "Functional Validation Requested: "
            f"{context.effective_configuration.functional_validation}"
        )

    for artifact in result.candidates:
        typer.echo(
            f"- {artifact.artifact_class.value}: {artifact.path}"
        )

    if result.validation:
        typer.echo(
            "Python Package Structural Validation: "
            f"{result.validation.status.value.upper()}"
        )

    if result.functional_validation:
        typer.echo(
            "Python Wheel Functional Validation: "
            f"{result.functional_validation.status.value.upper()}"
        )

    if result.diagnostic:
        typer.echo(
            result.diagnostic,
            err=True,
        )


def build(
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Directory for package-build outputs.",
        ),
    ] = DEFAULT_OUTPUT_DIR,
    functional_validation: Annotated[
        bool,
        typer.Option(
            "--functional-validation",
            help=(
                "Install and smoke-test the wheel in a clean temporary "
                "environment after static validation."
            ),
        ),
    ] = False,
    evidence_output: Annotated[
        Path | None,
        typer.Option(
            "--evidence-output",
            help=(
                "Write canonical Build Evidence as JSON after a "
                "successful build."
            ),
        ),
    ] = None,
) -> None:
    """Build the FamilyOS wheel and source distribution without publishing."""

    exit_code = run_package_build(
        output_dir,
        functional_validation=functional_validation,
        evidence_output=evidence_output,
    )

    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)
