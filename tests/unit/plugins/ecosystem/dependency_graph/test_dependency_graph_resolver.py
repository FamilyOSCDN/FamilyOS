"""Tests for the plugin dependency graph resolver."""

from unittest.mock import Mock

from familyos_cli.plugins.ecosystem.dependency_graph.cycle_detector import (
    CycleDetector,
)
from familyos_cli.plugins.ecosystem.dependency_graph.dependency_graph_resolver import (
    DependencyGraphResolver,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_dependency_graph import (
    PluginDependencyGraph,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.dependency_graph.topological_sorter import (
    TopologicalSorter,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)


def test_resolve_returns_cyclic_result_when_cycle_is_detected() -> None:
    """A detected cycle produces a global cycle diagnostic."""

    graph = Mock(
        spec=PluginDependencyGraph,
    )
    cycle_detector = Mock(
        spec=CycleDetector,
    )
    topological_sorter = Mock(
        spec=TopologicalSorter,
    )

    cycle_detector.has_cycle.return_value = True

    resolver = DependencyGraphResolver(
        cycle_detector=cycle_detector,
        topological_sorter=topological_sorter,
    )

    result = resolver.resolve(
        graph,
    )

    assert result.cycle_detected is True
    assert result.succeeded is False
    assert result.ordered_nodes == ()
    assert (
        len(
            result.diagnostics,
        )
        == 1
    )

    diagnostic = result.diagnostics[0]

    assert diagnostic.plugin is None
    assert diagnostic.message == "Dependency cycle detected."
    assert diagnostic.code is ResolutionDiagnosticCode.CYCLE_DETECTED
    assert diagnostic.severity is ResolutionDiagnosticSeverity.ERROR

    cycle_detector.has_cycle.assert_called_once_with(
        graph,
    )
    topological_sorter.sort.assert_not_called()


def test_resolve_returns_topologically_ordered_nodes() -> None:
    """An acyclic graph produces topologically ordered nodes."""

    graph = Mock(
        spec=PluginDependencyGraph,
    )
    first_node = Mock(
        spec=PluginNode,
    )
    second_node = Mock(
        spec=PluginNode,
    )
    ordered_nodes = (
        first_node,
        second_node,
    )

    cycle_detector = Mock(
        spec=CycleDetector,
    )
    topological_sorter = Mock(
        spec=TopologicalSorter,
    )

    cycle_detector.has_cycle.return_value = False
    topological_sorter.sort.return_value = ordered_nodes

    resolver = DependencyGraphResolver(
        cycle_detector=cycle_detector,
        topological_sorter=topological_sorter,
    )

    result = resolver.resolve(
        graph,
    )

    assert result.cycle_detected is False
    assert result.succeeded is True
    assert result.ordered_nodes == ordered_nodes
    assert result.diagnostics == ()

    cycle_detector.has_cycle.assert_called_once_with(
        graph,
    )
    topological_sorter.sort.assert_called_once_with(
        graph,
    )


def test_resolver_creates_default_algorithms() -> None:
    """The resolver creates default graph algorithms."""

    resolver = DependencyGraphResolver()

    assert isinstance(
        resolver._cycle_detector,
        CycleDetector,
    )
    assert isinstance(
        resolver._topological_sorter,
        TopologicalSorter,
    )
