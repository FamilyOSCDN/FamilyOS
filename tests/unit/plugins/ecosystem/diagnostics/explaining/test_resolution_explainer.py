"""Tests for the resolution explainer service."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
    ResolutionExplainer,
)


def make_diagnostic(
    kind: DiagnosticKind,
) -> PluginResolutionDiagnostic:
    """Create a diagnostic for testing."""

    return PluginResolutionDiagnostic(
        kind=kind,
        severity=DiagnosticSeverity.ERROR,
        message="Technical diagnostic.",
        plugin="familyos.security",
        details=("familyos.security depends on familyos.crypto",),
        path=(
            "familyos.security",
            "familyos.crypto",
            "familyos.security",
        ),
    )


def test_explains_missing_dependency() -> None:
    """Missing dependencies receive a specific explanation."""

    explanation = ResolutionExplainer().explain(
        make_diagnostic(
            DiagnosticKind.MISSING_DEPENDENCY,
        ),
    )

    assert explanation.title == ("Missing plugin dependency")
    assert explanation.has_suggestions()


def test_explains_version_conflict() -> None:
    """Version conflicts receive a specific explanation."""

    explanation = ResolutionExplainer().explain(
        make_diagnostic(
            DiagnosticKind.VERSION_CONFLICT,
        ),
    )

    assert explanation.title == ("Plugin version conflict")
    assert explanation.has_causes()


def test_explains_dependency_cycle() -> None:
    """Dependency cycles receive a specific explanation."""

    explanation = ResolutionExplainer().explain(
        make_diagnostic(
            DiagnosticKind.DEPENDENCY_CYCLE,
        ),
    )

    assert explanation.title == ("Dependency cycle detected")
    assert explanation.suggestions == ("Remove one dependency from the cycle.",)


def test_explains_unknown_diagnostic() -> None:
    """Unknown diagnostics receive a fallback explanation."""

    explanation = ResolutionExplainer().explain(
        make_diagnostic(
            DiagnosticKind.INFORMATION,
        ),
    )

    assert explanation.title == ("Plugin resolution issue")
    assert explanation.has_suggestions()
