"""Tests for suggestion generation."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.diagnostics.suggestions import (
    SuggestionGenerator,
)


def test_generates_missing_dependency_suggestion() -> None:
    """Missing dependency diagnostics produce a suggestion."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.MISSING_DEPENDENCY,
        severity=DiagnosticSeverity.ERROR,
        message="Missing dependency.",
    )

    suggestions = SuggestionGenerator().generate(
        diagnostic,
    )

    assert len(suggestions) == 1
    assert (
        suggestions[0].message
        == "Install the missing plugin or enable an appropriate repository."
    )


def test_generates_cycle_suggestion() -> None:
    """Dependency cycles produce a suggestion."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.DEPENDENCY_CYCLE,
        severity=DiagnosticSeverity.ERROR,
        message="Dependency cycle.",
    )

    suggestions = SuggestionGenerator().generate(
        diagnostic,
    )

    assert len(suggestions) == 1


def test_generates_version_conflict_suggestion() -> None:
    """Version conflicts produce a suggestion."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.VERSION_CONFLICT,
        severity=DiagnosticSeverity.ERROR,
        message="Version conflict.",
    )

    suggestions = SuggestionGenerator().generate(
        diagnostic,
    )

    assert len(suggestions) == 1


def test_returns_empty_for_unknown_kind() -> None:
    """Unknown diagnostics produce no suggestion."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.INFORMATION,
        severity=DiagnosticSeverity.INFO,
        message="Information.",
    )

    suggestions = SuggestionGenerator().generate(
        diagnostic,
    )

    assert suggestions == ()
