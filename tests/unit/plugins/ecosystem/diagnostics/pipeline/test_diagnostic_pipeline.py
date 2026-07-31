"""Tests for the plugin resolution diagnostic pipeline."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticPipeline,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution import (
    ResolutionDiagnostic,
    ResolutionPlan,
)


class FakeDiagnosticAdapter:
    """Diagnostic adapter returning predefined diagnostics."""

    def __init__(
        self,
        diagnostics: tuple[PluginResolutionDiagnostic, ...],
    ) -> None:
        self._diagnostics = diagnostics

    def adapt(
        self,
        plan: ResolutionPlan,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        return self._diagnostics


def make_diagnostic(
    plugin: str,
) -> PluginResolutionDiagnostic:
    """Create a diagnostic for pipeline tests."""

    return PluginResolutionDiagnostic(
        kind=DiagnosticKind.INFORMATION,
        severity=DiagnosticSeverity.INFO,
        message=f"Diagnostic for {plugin}.",
        plugin=plugin,
    )


def test_default_pipeline_builds_conflict_report() -> None:
    """The default pipeline includes resolution conflict diagnostics."""

    plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="security",
                message=(
                    "Required plugin dependency is not available."
                ),
            ),
        ],
    )

    report = DiagnosticPipeline().build(
        plan,
    )

    assert len(report.diagnostics) == 1
    assert report.diagnostics[0].plugin == "security"
    assert report.diagnostics[0].kind is (
        DiagnosticKind.MISSING_DEPENDENCY
    )
    assert report.has_errors()


def test_pipeline_returns_successful_empty_report() -> None:
    """A successful resolution produces an empty successful report."""

    report = DiagnosticPipeline().build(
        ResolutionPlan(),
    )

    assert report.is_empty()
    assert report.is_success()


def test_pipeline_aggregates_multiple_adapters() -> None:
    """The pipeline aggregates adapters in registration order."""

    first = make_diagnostic("security")
    second = make_diagnostic("backup")

    pipeline = DiagnosticPipeline(
        adapters=(
            FakeDiagnosticAdapter((first,)),
            FakeDiagnosticAdapter((second,)),
        ),
    )

    report = pipeline.build(
        ResolutionPlan(),
    )

    assert report.diagnostics == (
        first,
        second,
    )


def test_pipeline_accepts_no_registered_adapters() -> None:
    """An explicitly empty adapter collection produces an empty report."""

    pipeline = DiagnosticPipeline(
        adapters=(),
    )

    report = pipeline.build(
        ResolutionPlan(),
    )

    assert report.is_empty()
