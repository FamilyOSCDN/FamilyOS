"""Tests for the explanation rule registry."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticSeverity,
    ExplanationRuleRegistry,
    MissingDependencyRule,
    PluginResolutionDiagnostic,
    VersionConflictRule,
)


def diagnostic(
    kind: DiagnosticKind,
) -> PluginResolutionDiagnostic:
    """Create a diagnostic for testing."""

    return PluginResolutionDiagnostic(
        kind=kind,
        severity=DiagnosticSeverity.ERROR,
        message="Diagnostic",
    )


def test_registry_finds_matching_rule() -> None:
    """The registry returns the first compatible rule."""

    registry = ExplanationRuleRegistry(
        (
            MissingDependencyRule(),
            VersionConflictRule(),
        ),
    )

    rule = registry.find(
        diagnostic(
            DiagnosticKind.MISSING_DEPENDENCY,
        ),
    )

    assert isinstance(
        rule,
        MissingDependencyRule,
    )


def test_registry_preserves_rule_order() -> None:
    """Rules are evaluated in registration order."""

    registry = ExplanationRuleRegistry(
        (
            VersionConflictRule(),
            MissingDependencyRule(),
        ),
    )

    assert registry.rules()[0].__class__ is VersionConflictRule


def test_registry_returns_registered_rules() -> None:
    """The registry exposes its rules."""

    rules = (
        MissingDependencyRule(),
        VersionConflictRule(),
    )

    registry = ExplanationRuleRegistry(
        rules,
    )

    assert registry.rules() == rules
