"""Tests for plugin dependency graph resolution results."""

from unittest.mock import Mock

from familyos_cli.plugins.ecosystem.dependency_graph.dependency_resolution_result import (
    DependencyResolutionResult,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)


def test_resolved_result_contains_ordered_nodes() -> None:
    first_node = Mock(
        spec=PluginNode,
    )
    second_node = Mock(
        spec=PluginNode,
    )

    result = DependencyResolutionResult.resolved(
        (
            first_node,
            second_node,
        ),
    )

    assert result.ordered_nodes == (
        first_node,
        second_node,
    )
    assert result.cycle_detected is False
    assert result.diagnostics == ()
    assert result.succeeded is True


def test_resolved_result_can_contain_non_error_diagnostics() -> None:
    node = Mock(
        spec=PluginNode,
    )
    diagnostic = ResolutionDiagnostic(
        plugin="example",
        message="Optional dependency is unavailable.",
        code=ResolutionDiagnosticCode.WARNING,
        severity=ResolutionDiagnosticSeverity.WARNING,
    )

    result = DependencyResolutionResult.resolved(
        ordered_nodes=(
            node,
        ),
        diagnostics=(
            diagnostic,
        ),
    )

    assert result.ordered_nodes == (
        node,
    )
    assert result.cycle_detected is False
    assert result.diagnostics == (
        diagnostic,
    )
    assert result.succeeded is True


def test_result_with_error_diagnostic_is_not_successful() -> None:
    diagnostic = ResolutionDiagnostic(
        plugin="example",
        message="Missing dependency.",
        code=ResolutionDiagnosticCode.MISSING_DEPENDENCY,
        severity=ResolutionDiagnosticSeverity.ERROR,
    )

    result = DependencyResolutionResult.resolved(
        ordered_nodes=(),
        diagnostics=(
            diagnostic,
        ),
    )

    assert result.cycle_detected is False
    assert result.diagnostics == (
        diagnostic,
    )
    assert result.succeeded is False


def test_cyclic_result_contains_cycle_diagnostic() -> None:
    result = DependencyResolutionResult.cyclic()

    assert result.ordered_nodes == ()
    assert result.cycle_detected is True
    assert result.succeeded is False
    assert len(
        result.diagnostics,
    ) == 1

    diagnostic = result.diagnostics[0]

    assert diagnostic.plugin == ""
    assert diagnostic.message == "Dependency cycle detected."
    assert diagnostic.code is ResolutionDiagnosticCode.CYCLE_DETECTED
    assert diagnostic.severity is ResolutionDiagnosticSeverity.ERROR
    assert diagnostic.is_error is True
