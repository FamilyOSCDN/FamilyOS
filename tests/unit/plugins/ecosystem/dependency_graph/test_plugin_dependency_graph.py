"""Tests for plugin dependency graph."""

from familyos_cli.plugins.ecosystem.dependency_graph.dependency_edge import (
    DependencyEdge,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_dependency_graph import (
    PluginDependencyGraph,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def make_node(name: str) -> PluginNode:
    return PluginNode(
        package=PluginPackage(
            plugin_id=f"familyos.{name}",
            version="1.0.0",
            source="test",
        ),
    )


def test_add_node() -> None:
    graph = PluginDependencyGraph()
    node = make_node("documentation")

    graph.add_node(node)

    assert graph.contains(node)


def test_duplicate_node_is_ignored() -> None:
    graph = PluginDependencyGraph()
    node = make_node("documentation")

    graph.add_node(node)
    graph.add_node(node)

    assert len(graph.nodes) == 1


def test_add_edge_adds_nodes() -> None:
    graph = PluginDependencyGraph()

    source = make_node("documentation")
    target = make_node("security")

    graph.add_edge(
        DependencyEdge(
            source,
            target,
        ),
    )

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1


def test_outgoing_edges() -> None:
    graph = PluginDependencyGraph()

    source = make_node("documentation")
    target = make_node("security")

    edge = DependencyEdge(
        source,
        target,
    )

    graph.add_edge(edge)

    assert graph.outgoing_edges(source) == (edge,)


def test_incoming_edges() -> None:
    graph = PluginDependencyGraph()

    source = make_node("documentation")
    target = make_node("security")

    edge = DependencyEdge(
        source,
        target,
    )

    graph.add_edge(edge)

    assert graph.incoming_edges(target) == (edge,)


def test_duplicate_edge_is_ignored() -> None:
    graph = PluginDependencyGraph()

    source = make_node("documentation")
    target = make_node("security")

    edge = DependencyEdge(
        source,
        target,
    )

    graph.add_edge(edge)
    graph.add_edge(edge)

    assert len(graph.edges) == 1
