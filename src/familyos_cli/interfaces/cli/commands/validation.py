"""Canonical validation commands."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.application.validation import CiValidationResult
from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.interfaces.cli.rendering.ci_validation_json import (
    CiValidationJsonRenderer,
)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
CANONICAL_CI_ARTIFACT = "ci-validation.json"
_SUPPORTED_FORMATS = {"text", "json"}

validation_app = typer.Typer(
    help="Canonical repository validation commands.",
    no_args_is_help=True,
)


def run_ci_validation(
    *,
    output_format: str,
    output_path: Path | None,
) -> int:
    """Execute canonical CI validation and render its complete result."""

    if output_format not in _SUPPORTED_FORMATS:
        Output.error(
            f"Unsupported format '{output_format}'. Use 'text' or 'json'.",
        )
        return EXIT_FAILURE

    result = CommandContext().run_ci_validation.execute()
    rendered_json = CiValidationJsonRenderer().render(result)

    if output_path is not None:
        output_path.write_text(rendered_json, encoding="utf-8")

    if output_format == "json":
        typer.echo(rendered_json, nl=False)
    else:
        typer.echo(_render_text(result))

    return EXIT_SUCCESS if result.successful else EXIT_FAILURE


def _render_text(result: CiValidationResult) -> str:
    lines = [f"Canonical CI Validation: {result.status.value.upper()}"]
    for gate in result.gates:
        lines.append(f"- {gate.gate_id}: {gate.status.value.upper()}")
        if gate.diagnostic:
            lines.append(f"  {gate.diagnostic}")
        if gate.profile_id:
            lines.append(f"  profile: {gate.profile_id}")
            lines.extend(
                f"  - {plugin.plugin_id}: {plugin.status.upper()}"
                for plugin in gate.plugins
            )
    return "\n".join(lines)


@validation_app.command(name="ci")
def ci(
    output_format: Annotated[
        str,
        typer.Option(
            "--format",
            help="Output format: 'text' or 'json'.",
        ),
    ] = "text",
    output_path: Annotated[
        Path | None,
        typer.Option(
            "--output",
            help=f"Write canonical JSON evidence (normally {CANONICAL_CI_ARTIFACT}).",
        ),
    ] = None,
) -> None:
    """Run the canonical FamilyOS CI validation profile."""

    exit_code = run_ci_validation(
        output_format=output_format,
        output_path=output_path,
    )
    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)
