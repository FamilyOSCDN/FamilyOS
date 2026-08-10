"""Tests for dependency graph edges."""

import pytest

from familyos_cli.plugins.ecosystem.dependency_graph.dependency_edge import (
    DependencyEdge,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)


def make_node(
    name: str,
    version: str,
) -> PluginNode:
    """Create a graph node for testing."""

    return PluginNode(
        package=PluginPackage(
            name=name,
            version=version,
            source="test",
        ),
    )


def test_edge_contains_source_and_target() -> None:
    source = make_node(
        "familyos.documentation",
        "1.0.0",
    )
    target = make_node(
        "familyos.security",
        "2.0.0",
    )

    edge = DependencyEdge(
        source=source,
        target=target,
    )

    assert edge.source is source
    assert edge.target is target


def test_edge_dependency_is_optional() -> None:
    edge = DependencyEdge(
        source=make_node(
            "familyos.documentation",
            "1.0.0",
        ),
        target=make_node(
            "familyos.security",
            "2.0.0",
        ),
    )

    assert edge.dependency is None


def test_edge_contains_dependency_requirement() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.security",
        minimum_version="2.0.0",
    )

    edge = DependencyEdge(
        source=make_node(
            "familyos.documentation",
            "1.0.0",
        ),
        target=make_node(
            "familyos.security",
            "2.1.0",
        ),
        dependency=dependency,
    )

    assert edge.dependency is dependency


def test_edge_rejects_requirement_for_another_target() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.notification",
        minimum_version="1.0.0",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Dependency edge requirement must reference "
            "target plugin 'familyos.security'."
        ),
    ):
        DependencyEdge(
            source=make_node(
                "familyos.documentation",
                "1.0.0",
            ),
            target=make_node(
                "familyos.security",
                "2.0.0",
            ),
            dependency=dependency,
        )


def test_edge_identifier() -> None:
    edge = DependencyEdge(
        source=make_node(
            "familyos.documentation",
            "1.0.0",
        ),
        target=make_node(
            "familyos.security",
            "2.0.0",
        ),
    )

    assert edge.identifier() == "familyos.documentation@1.0.0->familyos.security@2.0.0"


def test_equal_edges_compare_equal() -> None:
    source = make_node(
        "familyos.documentation",
        "1.0.0",
    )
    target = make_node(
        "familyos.security",
        "2.0.0",
    )
    dependency = PluginDependency(
        plugin_id="familyos.security",
        minimum_version="2.0.0",
    )

    first = DependencyEdge(
        source=source,
        target=target,
        dependency=dependency,
    )
    second = DependencyEdge(
        source=source,
        target=target,
        dependency=dependency,
    )

    assert first == second


def test_edges_with_different_requirements_compare_different() -> None:
    source = make_node(
        "familyos.documentation",
        "1.0.0",
    )
    target = make_node(
        "familyos.security",
        "2.0.0",
    )

    first = DependencyEdge(
        source=source,
        target=target,
        dependency=PluginDependency(
            plugin_id="familyos.security",
            minimum_version="1.0.0",
        ),
    )
    second = DependencyEdge(
        source=source,
        target=target,
        dependency=PluginDependency(
            plugin_id="familyos.security",
            minimum_version="2.0.0",
        ),
    )

    assert first != second


def test_different_edges_compare_different() -> None:
    edge_one = DependencyEdge(
        source=make_node(
            "familyos.documentation",
            "1.0.0",
        ),
        target=make_node(
            "familyos.security",
            "2.0.0",
        ),
    )

    edge_two = DependencyEdge(
        source=make_node(
            "familyos.documentation",
            "1.0.0",
        ),
        target=make_node(
            "familyos.notification",
            "2.0.0",
        ),
    )

    assert edge_one != edge_two


def test_edge_is_hashable() -> None:
    edge = DependencyEdge(
        source=make_node(
            "familyos.documentation",
            "1.0.0",
        ),
        target=make_node(
            "familyos.security",
            "2.0.0",
        ),
        dependency=PluginDependency(
            plugin_id="familyos.security",
            minimum_version="2.0.0",
        ),
    )

    edges = {
        edge,
    }

    assert edge in edges


def test_self_dependency_is_supported_by_model() -> None:
    node = make_node(
        "familyos.documentation",
        "1.0.0",
    )

    edge = DependencyEdge(
        source=node,
        target=node,
        dependency=PluginDependency(
            plugin_id="familyos.documentation",
            minimum_version="1.0.0",
        ),
    )

    assert edge.source is node
    assert edge.target is node
