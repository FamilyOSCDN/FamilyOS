"""Plugin compliance command."""

from __future__ import annotations

from typing import Annotated

import typer

from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.json_compliance_renderer import (
    JsonComplianceRenderer,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.text_compliance_renderer import (
    TextComplianceRenderer,
)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

_SUPPORTED_FORMATS = {"text", "json"}

compliance_app = typer.Typer(
    help="Plugin compliance commands.",
    no_args_is_help=True,
)


def plugin_compliance_check(
    *,
    plugin_id: str,
    profile_id: str,
    output_format: str,
) -> int:
    """Check plugin compliance and render the report.

    Returns:
        Zero when the plugin is COMPLIANT, one otherwise (including
        expected input errors presented to the user).
    """

    if output_format not in _SUPPORTED_FORMATS:
        Output.error(
            f"Unsupported format '{output_format}'. Use 'text' or 'json'.",
        )

        return EXIT_FAILURE

    context = CommandContext()

    try:
        report = context.check_plugin_compliance.execute(
            plugin_id=plugin_id,
            profile_id=profile_id,
        )
    except ValueError as error:
        Output.error(
            str(error),
        )

        return EXIT_FAILURE

    renderer = (
        JsonComplianceRenderer()
        if output_format == "json"
        else TextComplianceRenderer()
    )

    typer.echo(
        renderer.render(report),
    )

    if report.result.status is ComplianceStatus.COMPLIANT:
        return EXIT_SUCCESS

    return EXIT_FAILURE


@compliance_app.command(
    name="check",
)
def check(
    plugin_id: Annotated[
        str,
        typer.Argument(
            ...,
            help="Canonical plugin identifier, e.g. 'familyos.security'.",
        ),
    ],
    profile: Annotated[
        str,
        typer.Option(
            "--profile",
            help="Compliance profile to evaluate against.",
        ),
    ] = "official",
    output_format: Annotated[
        str,
        typer.Option(
            "--format",
            help="Report format: 'text' or 'json'.",
        ),
    ] = "text",
) -> None:
    """Check a plugin's compliance against a profile."""

    exit_code = plugin_compliance_check(
        plugin_id=plugin_id,
        profile_id=profile,
        output_format=output_format,
    )

    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(
            code=exit_code,
        )
