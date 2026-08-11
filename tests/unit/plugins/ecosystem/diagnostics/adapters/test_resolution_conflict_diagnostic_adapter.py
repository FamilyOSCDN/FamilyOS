"""Tests for the composite resolution conflict diagnostic adapter."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    ResolutionConflictDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.resolution import (
    ResolutionDiagnostic,
    ResolutionPlan,
)


def test_adapter_builds_diagnostic_from_resolution_plan() -> None:
    """The composite adapter maps resolver output to diagnostics."""

    plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.security",
                message=("Required plugin dependency is not available."),
            ),
        ],
    )

    diagnostics = ResolutionConflictDiagnosticAdapter().adapt(
        plan,
    )

    assert len(diagnostics) == 1
    assert diagnostics[0].plugin == "familyos.security"
    assert diagnostics[0].kind is DiagnosticKind.MISSING_DEPENDENCY


def test_adapter_returns_empty_tuple_for_successful_plan() -> None:
    """A successful plan produces no conflict diagnostics."""

    diagnostics = ResolutionConflictDiagnosticAdapter().adapt(
        ResolutionPlan(),
    )

    assert diagnostics == ()
