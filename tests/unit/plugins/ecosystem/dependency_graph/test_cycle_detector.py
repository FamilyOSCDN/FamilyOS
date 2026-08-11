"""Tests for plugin dependency graph cycle detection."""

from familyos_cli.plugins.ecosystem.dependency_graph.cycle_detector import (
    CycleDetector,
)
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


def test_empty_graph_has_no_cycle() -> None:
    graph = PluginDependencyGraph()

    assert not CycleDetector().has_cycle(
        graph,
    )


def test_single_node_without_edge_has_no_cycle() -> None:
    graph = PluginDependencyGraph()
    graph.add_node(
        make_node("core"),
    )

    assert not CycleDetector().has_cycle(
        graph,
    )


def test_single_self_dependency_has_cycle() -> None:
    graph = PluginDependencyGraph()
    node = make_node(
        "core",
    )

    graph.add_edge(
        DependencyEdge(
            source=node,
            target=node,
        ),
    )

    assert CycleDetector().has_cycle(
        graph,
    )


def test_linear_dependency_chain_has_no_cycle() -> None:
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

    graph.add_edge(
        DependencyEdge(
            source=documentation,
            target=security,
        ),
    )
    graph.add_edge(
        DependencyEdge(
            source=security,
            target=core,
        ),
    )

    assert not CycleDetector().has_cycle(
        graph,
    )


def test_two_node_cycle_is_detected() -> None:
    graph = PluginDependencyGraph()

    core = make_node(
        "core",
    )
    security = make_node(
        "security",
    )

    graph.add_edge(
        DependencyEdge(
            source=core,
            target=security,
        ),
    )
    graph.add_edge(
        DependencyEdge(
            source=security,
            target=core,
        ),
    )

    assert CycleDetector().has_cycle(
        graph,
    )


def test_three_node_cycle_is_detected() -> None:
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

    graph.add_edge(
        DependencyEdge(
            source=core,
            target=security,
        ),
    )
    graph.add_edge(
        DependencyEdge(
            source=security,
            target=documentation,
        ),
    )
    graph.add_edge(
        DependencyEdge(
            source=documentation,
            target=core,
        ),
    )

    assert CycleDetector().has_cycle(
        graph,
    )


def test_cycle_in_disconnected_component_is_detected() -> None:
    graph = PluginDependencyGraph()

    standalone = make_node(
        "standalone",
    )
    core = make_node(
        "core",
    )
    security = make_node(
        "security",
    )

    graph.add_node(
        standalone,
    )
    graph.add_edge(
        DependencyEdge(
            source=core,
            target=security,
        ),
    )
    graph.add_edge(
        DependencyEdge(
            source=security,
            target=core,
        ),
    )

    assert CycleDetector().has_cycle(
        graph,
    )


def test_shared_dependency_without_cycle() -> None:
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

    graph.add_edge(
        DependencyEdge(
            source=security,
            target=core,
        ),
    )
    graph.add_edge(
        DependencyEdge(
            source=documentation,
            target=core,
        ),
    )

    assert not CycleDetector().has_cycle(
        graph,
    )
