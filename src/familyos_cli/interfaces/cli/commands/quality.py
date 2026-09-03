"""Quality Framework CLI commands."""

from __future__ import annotations

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
