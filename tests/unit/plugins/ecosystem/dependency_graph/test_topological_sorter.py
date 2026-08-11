"""Tests for plugin dependency graph topological sorting."""

import pytest

from familyos_cli.plugins.ecosystem.dependency_graph.dependency_edge import (
    DependencyEdge,
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
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def make_node(
    name: str,
) -> PluginNode:
    """Create a graph node for testing."""

    return PluginNode(
        package=PluginPackage(
            plugin_id=f"familyos.{name}",
            version="1.0.0",
            source="test",
        ),
    )


def add_dependency(
    graph: PluginDependencyGraph,
    dependent: PluginNode,
    dependency: PluginNode,
) -> None:
    """Add a directed dependency to a graph."""

    graph.add_edge(
        DependencyEdge(
            source=dependent,
            target=dependency,
        ),
    )


def test_empty_graph_returns_empty_order() -> None:
    graph = PluginDependencyGraph()

    result = TopologicalSorter().sort(
        graph,
    )

    assert result == ()


def test_single_node_is_returned() -> None:
    graph = PluginDependencyGraph()
    core = make_node(
        "core",
    )

    graph.add_node(
        core,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result == (core,)


def test_dependency_is_placed_before_dependent() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    security = make_node(
        "security",
    )

    add_dependency(
        graph=graph,
        dependent=security,
        dependency=core,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result == (
        core,
        security,
    )


def test_linear_chain_is_sorted_dependency_first() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    security = make_node(
        "security",
    )
    documentation = make_node(
        "documentation",
    )

    add_dependency(
        graph=graph,
        dependent=security,
        dependency=core,
    )
    add_dependency(
        graph=graph,
        dependent=documentation,
        dependency=security,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result == (
        core,
        security,
        documentation,
    )


def test_shared_dependency_precedes_all_dependents() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    documentation = make_node(
        "documentation",
    )
    security = make_node(
        "security",
    )

    add_dependency(
        graph=graph,
        dependent=documentation,
        dependency=core,
    )
    add_dependency(
        graph=graph,
        dependent=security,
        dependency=core,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result[0] == core
    assert result.index(core) < result.index(documentation)
    assert result.index(core) < result.index(security)


def test_multiple_dependencies_precede_dependent() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    security = make_node(
        "security",
    )
    documentation = make_node(
        "documentation",
    )

    add_dependency(
        graph=graph,
        dependent=documentation,
        dependency=core,
    )
    add_dependency(
        graph=graph,
        dependent=documentation,
        dependency=security,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result.index(core) < result.index(documentation)
    assert result.index(security) < result.index(documentation)


def test_disconnected_nodes_are_sorted_deterministically() -> None:
    graph = PluginDependencyGraph()

    security = make_node(
        "security",
    )
    core = make_node(
        "core",
    )
    documentation = make_node(
        "documentation",
    )

    graph.add_node(
        security,
    )
    graph.add_node(
        core,
    )
    graph.add_node(
        documentation,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result == (
        core,
        documentation,
        security,
    )


def test_independent_ready_nodes_use_identifier_order() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    alpha = make_node(
        "alpha",
    )
    beta = make_node(
        "beta",
    )

    add_dependency(
        graph=graph,
        dependent=beta,
        dependency=core,
    )
    add_dependency(
        graph=graph,
        dependent=alpha,
        dependency=core,
    )

    result = TopologicalSorter().sort(
        graph,
    )

    assert result == (
        core,
        alpha,
        beta,
    )


def test_two_node_cycle_raises_value_error() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    security = make_node(
        "security",
    )

    add_dependency(
        graph=graph,
        dependent=core,
        dependency=security,
    )
    add_dependency(
        graph=graph,
        dependent=security,
        dependency=core,
    )

    with pytest.raises(
        ValueError,
        match=("Cannot topologically sort a dependency graph containing a cycle."),
    ):
        TopologicalSorter().sort(
            graph,
        )


def test_self_dependency_raises_value_error() -> None:
    graph = PluginDependencyGraph()
    core = make_node(
        "core",
    )

    add_dependency(
        graph=graph,
        dependent=core,
        dependency=core,
    )

    with pytest.raises(
        ValueError,
        match=("Cannot topologically sort a dependency graph containing a cycle."),
    ):
        TopologicalSorter().sort(
            graph,
        )
