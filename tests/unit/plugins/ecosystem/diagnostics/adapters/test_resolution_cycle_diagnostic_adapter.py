"""Tests for the resolution cycle diagnostic adapter."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticSeverity,
    ResolutionContext,
    ResolutionCycleDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.resolution import ResolutionPlan


class FakeCycleDetectionSource:
    """Simple dependency graph source for resolution diagnostics."""

    def plugins(self) -> tuple[str, ...]:
        """Return plugins in the dependency graph."""

        return (
            "familyos.security",
            "familyos.crypto",
        )

    def dependencies_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        """Return dependencies of a plugin."""

        if plugin == "familyos.security":
            return ("familyos.crypto",)

        if plugin == "familyos.crypto":
            return ("familyos.security",)

        return ()


class FakeAcyclicCycleDetectionSource:
    """Acyclic dependency graph source."""

    def plugins(self) -> tuple[str, ...]:
        """Return plugins in the dependency graph."""

        return (
            "familyos.security",
            "familyos.crypto",
        )

    def dependencies_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        """Return dependencies of a plugin."""

        if plugin == "familyos.security":
            return ("familyos.crypto",)

        return ()


def test_adapter_returns_empty_tuple_without_cycle_source() -> None:
    """No cycle source produces no cycle diagnostics."""

    context = ResolutionContext(
        plan=ResolutionPlan(),
    )

    diagnostics = ResolutionCycleDiagnosticAdapter().adapt(
        context,
    )

    assert diagnostics == ()


def test_adapter_detects_dependency_cycle() -> None:
    """A dependency cycle becomes a resolution diagnostic."""

    context = ResolutionContext(
        plan=ResolutionPlan(),
        cycle_source=FakeCycleDetectionSource(),
    )

    diagnostics = ResolutionCycleDiagnosticAdapter().adapt(
        context,
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.kind is DiagnosticKind.DEPENDENCY_CYCLE
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.plugin == "familyos.crypto"
    assert diagnostic.message == ("Plugin dependency cycle detected.")
    assert diagnostic.path == (
        "familyos.crypto",
        "familyos.security",
        "familyos.crypto",
    )
    assert diagnostic.details == (
        "Dependency path: familyos.crypto -> familyos.security -> familyos.crypto",
    )


def test_adapter_ignores_acyclic_dependency_graph() -> None:
    """An acyclic dependency graph produces no diagnostics."""

    context = ResolutionContext(
        plan=ResolutionPlan(),
        cycle_source=FakeAcyclicCycleDetectionSource(),
    )

    diagnostics = ResolutionCycleDiagnosticAdapter().adapt(
        context,
    )

    assert diagnostics == ()
