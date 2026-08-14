"""Canonical FamilyOS package-build command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.application.build import CanonicalPackageBuildResult
from familyos_cli.interfaces.cli.context import CommandContext

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
DEFAULT_OUTPUT_DIR = Path("dist")


def run_package_build(output_dir: Path) -> int:
    """Execute and render the canonical package build."""

    result = CommandContext().run_package_build.execute(output_dir)
    _render_result(result)
    return EXIT_SUCCESS if result.successful else EXIT_FAILURE


def _render_result(result: CanonicalPackageBuildResult) -> None:
    """Render process-level build output without trust claims."""

    typer.echo(f"Canonical Package Build: {result.status.value.upper()}")
    for artifact in result.candidates:
        typer.echo(f"- {artifact.artifact_class.value}: {artifact.path}")
    if result.diagnostic:
        typer.echo(result.diagnostic, err=True)


def build(
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Directory for package-build outputs.",
        ),
    ] = DEFAULT_OUTPUT_DIR,
) -> None:
    """Build the FamilyOS wheel and source distribution without publishing."""

    exit_code = run_package_build(output_dir)
    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)
