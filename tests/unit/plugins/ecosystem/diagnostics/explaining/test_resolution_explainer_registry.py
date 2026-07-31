"""Tests for explainer registry integration."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
    ResolutionExplainer,
)


def test_explainer_uses_registered_rules() -> None:
    """The explainer delegates explanation creation."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.MISSING_DEPENDENCY,
        severity=DiagnosticSeverity.ERROR,
        message="Missing dependency.",
    )

    explanation = ResolutionExplainer().explain(
        diagnostic,
    )

    assert explanation.title == (
        "Missing plugin dependency"
    )
