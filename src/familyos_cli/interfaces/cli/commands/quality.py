"""Quality Framework CLI commands."""

from __future__ import annotations

import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentState,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.interfaces.cli.quality_report_output import write_quality_report
from familyos_cli.interfaces.cli.rendering.quality_report_json import (
    QualityReportJsonRenderer,
)

EXIT_SUCCESS = 0
EXIT_QUALITY_FAIL = 1
EXIT_QUALITY_ERROR = 2
_UNRELIABLE_STATUSES = {
    QualityStatus.ERROR,
    QualityStatus.UNKNOWN,
    QualityStatus.SKIPPED,
}
quality_app = typer.Typer(help="Quality Framework commands.", no_args_is_help=True)


def _exit_code(results: tuple[QualityCheckResult, ...]) -> int:
    if not results:
        return EXIT_QUALITY_ERROR
    statuses = {result.status for result in results}
    if statuses & _UNRELIABLE_STATUSES:
        return EXIT_QUALITY_ERROR
    if QualityStatus.FAIL in statuses:
        return EXIT_QUALITY_FAIL
    return EXIT_SUCCESS


def _render_results(results: tuple[QualityCheckResult, ...]) -> None:
    for result in results:
        typer.echo(f"{result.check_id}: {result.status.value.upper()}")


@quality_app.command(name="check")
def check(
    target_type: Annotated[
        str, typer.Option("--target-type", help="Canonical Quality target type.")
    ],
    identifier: Annotated[
        str, typer.Option("--identifier", help="Canonical Quality target identifier.")
    ],
    path: Annotated[str, typer.Option("--path", help="Canonical Quality target path.")],
    revision: Annotated[
        str | None,
        typer.Option("--revision", help="Optional canonical target revision."),
    ] = None,
    version: Annotated[
        str | None, typer.Option("--version", help="Optional canonical target version.")
    ] = None,
) -> None:
    """Execute governed Quality checks for an explicit target."""
    try:
        target = QualityTarget(
            target_type=target_type,
            identifier=identifier,
            path=path,
            revision=revision,
            version=version,
        )
        results = CommandContext().quality_execution.execute(target)
    except (TypeError, ValueError) as exc:
        Output.error(str(exc))
        raise typer.Exit(code=EXIT_QUALITY_ERROR) from None
    _render_results(results)
    exit_code = _exit_code(results)
    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)


def _assessment_exit_code(assessment: QualityAssessment) -> int:
    if assessment.status in (QualityStatus.ERROR, QualityStatus.UNKNOWN):
        return EXIT_QUALITY_ERROR
    if assessment.quality_state in (
        QualityAssessmentState.PASS,
        QualityAssessmentState.PASS_WITH_WARNINGS,
    ):
        return EXIT_SUCCESS
    if assessment.quality_state is QualityAssessmentState.FAIL:
        return EXIT_QUALITY_FAIL
    return EXIT_QUALITY_ERROR


def _render_assessment(assessment: QualityAssessment) -> None:
    typer.echo(f"Assessment ID: {assessment.id}")
    typer.echo(
        f"Target: {assessment.target.target_type}:{assessment.target.identifier}"
    )
    if assessment.revision is not None:
        typer.echo(f"Revision: {assessment.revision}")
    typer.echo(f"Profile: {assessment.profile}")
    typer.echo(f"Status: {assessment.status.value}")
    typer.echo(f"Quality State: {assessment.quality_state.value}")
    typer.echo(
        "Evidence IDs: " + (", ".join(str(v) for v in assessment.evidence_ids) or "-")
    )
    typer.echo(
        "Finding IDs: " + (", ".join(str(v) for v in assessment.finding_ids) or "-")
    )
    typer.echo(f"Created At: {assessment.created_at.isoformat()}")


@quality_app.command(name="assess")
def assess(
    target_type: Annotated[
        str, typer.Option("--target-type", help="Canonical Quality target type.")
    ],
    identifier: Annotated[
        str, typer.Option("--identifier", help="Canonical Quality target identifier.")
    ],
    path: Annotated[str, typer.Option("--path", help="Canonical Quality target path.")],
    revision: Annotated[
        str | None,
        typer.Option("--revision", help="Optional canonical target revision."),
    ] = None,
    version: Annotated[
        str | None, typer.Option("--version", help="Optional canonical target version.")
    ] = None,
) -> None:
    try:
        target = QualityTarget(
            target_type=target_type,
            identifier=identifier,
            path=path,
            revision=revision,
            version=version,
        )
        assessment = CommandContext().quality_assessment.execute(target)
    except (TypeError, ValueError) as exc:
        Output.error(str(exc))
        raise typer.Exit(code=EXIT_QUALITY_ERROR) from None
    _render_assessment(assessment)
    exit_code = _assessment_exit_code(assessment)
    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)


def _render_report(assessment: QualityAssessment) -> None:
    """Present canonical assessment fields in a stable order."""
    target = assessment.target
    lines = [
        f"Assessment ID: {assessment.id}",
        f"Target: {target.target_type}:{target.identifier}",
    ]
    if target.path is not None:
        lines.append(f"Path: {target.path}")
    if target.revision is not None:
        lines.append(f"Revision: {target.revision}")
    if target.version is not None:
        lines.append(f"Version: {target.version}")
    lines.extend(
        (
            f"Profile: {assessment.profile}",
            f"Status: {assessment.status.value}",
            f"Quality State: {assessment.quality_state.value}",
            "Evidence IDs: "
            + (", ".join(str(value) for value in assessment.evidence_ids) or "-"),
            "Finding IDs: "
            + (", ".join(str(value) for value in assessment.finding_ids) or "-"),
            f"Created At: {assessment.created_at.isoformat()}",
        )
    )
    typer.echo("\n".join(lines))


@quality_app.command(name="report")
def report(
    target_type: Annotated[
        str, typer.Option("--target-type", help="Canonical Quality target type.")
    ],
    identifier: Annotated[
        str, typer.Option("--identifier", help="Canonical Quality target identifier.")
    ],
    path: Annotated[str, typer.Option("--path", help="Canonical Quality target path.")],
    revision: Annotated[
        str | None,
        typer.Option("--revision", help="Optional canonical target revision."),
    ] = None,
    version: Annotated[
        str | None, typer.Option("--version", help="Optional canonical target version.")
    ] = None,
    output_format: Annotated[
        str, typer.Option("--format", help="Report format: 'text' or 'json'.")
    ] = "text",
    output_path: Annotated[
        str | None, typer.Option("--output", help="Write JSON atomically to PATH; '-' means stdout.")
    ] = None,
) -> None:
    """Execute a governed assessment and render its canonical Quality report."""
    if output_format not in {"text", "json"}:
        Output.diagnostic("Unsupported Quality report format. Use 'text' or 'json'.")
        raise typer.Exit(code=EXIT_QUALITY_ERROR)
    if output_path is not None and (not output_path or output_format != "json"):
        Output.diagnostic("--output requires JSON format and a non-empty path.")
        raise typer.Exit(code=EXIT_QUALITY_ERROR)
    if output_format == "json":
        _report_json(target_type, identifier, path, revision, version, output_path)
        return
    try:
        target = QualityTarget(
            target_type=target_type,
            identifier=identifier,
            path=path,
            revision=revision,
            version=version,
        )
        assessment = CommandContext().quality_assessment.execute(target)
    except (TypeError, ValueError) as exc:
        Output.error(str(exc))
        raise typer.Exit(code=EXIT_QUALITY_ERROR) from None

    try:
        _render_report(assessment)
    except Exception as exc:
        # The report contract classifies rendering failures as CLI errors.
        Output.error(f"Quality report rendering failed: {exc}")
        raise typer.Exit(code=EXIT_QUALITY_ERROR) from None

    exit_code = _assessment_exit_code(assessment)
    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)


def _report_json(
    target_type: str, identifier: str, path: str,
    revision: str | None, version: str | None, output_path: str | None,
) -> None:
    """Keep machine-readable output separate from execution diagnostics."""
    try:
        target = QualityTarget(
            target_type=target_type, identifier=identifier, path=path,
            revision=revision, version=version,
        )
        with redirect_stdout(sys.stderr):
            result = CommandContext().quality_assessment.execute_with_results(target)
        rendered = QualityReportJsonRenderer().render(result)
        if output_path is None or output_path == "-":
            typer.echo(rendered, nl=False)
        else:
            write_quality_report(Path(output_path), rendered)
        exit_code = _assessment_exit_code(result.assessment)
    except Exception as exc:
        Output.diagnostic(f"Quality JSON report failed: {exc}")
        raise typer.Exit(code=EXIT_QUALITY_ERROR) from None
    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)
