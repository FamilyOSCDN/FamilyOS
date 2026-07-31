"""Tests for the dependency cycle diagnostic adapter."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    CycleDiagnosticAdapter,
    DependencyCycle,
    DiagnosticKind,
    DiagnosticSeverity,
)


def test_cycle_adapter_creates_dependency_cycle_diagnostic() -> None:
    """A dependency cycle becomes a diagnostic."""

    cycle = DependencyCycle(
        path=(
            "security",
            "crypto",
            "security",
        ),
    )

    diagnostics = CycleDiagnosticAdapter().adapt(
        (cycle,),
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.kind is DiagnosticKind.DEPENDENCY_CYCLE
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.plugin == "security"
    assert diagnostic.message == (
        "Plugin dependency cycle detected."
    )
    assert diagnostic.path == (
        "security",
        "crypto",
        "security",
    )
    assert diagnostic.details == (
        "Dependency path: security -> crypto -> security",
    )


def test_cycle_adapter_returns_empty_tuple_for_no_cycles() -> None:
    """No cycles produce no diagnostics."""

    diagnostics = CycleDiagnosticAdapter().adapt(
        (),
    )

    assert diagnostics == ()


def test_cycle_adapter_preserves_multiple_cycles_order() -> None:
    """Multiple cycles preserve their original order."""

    diagnostics = CycleDiagnosticAdapter().adapt(
        (
            DependencyCycle(
                path=(
                    "security",
                    "crypto",
                    "security",
                ),
            ),
            DependencyCycle(
                path=(
                    "backup",
                    "storage",
                    "backup",
                ),
            ),
        ),
    )

    assert tuple(
        diagnostic.plugin
        for diagnostic in diagnostics
    ) == (
        "security",
        "backup",
    )


def test_cycle_adapter_keeps_cycle_path_information() -> None:
    """Cycle path remains available for explanations."""

    diagnostic = CycleDiagnosticAdapter().adapt(
        (
            DependencyCycle(
                path=(
                    "a",
                    "b",
                    "c",
                    "a",
                ),
            ),
        ),
    )[0]

    assert diagnostic.path == (
        "a",
        "b",
        "c",
        "a",
    )
