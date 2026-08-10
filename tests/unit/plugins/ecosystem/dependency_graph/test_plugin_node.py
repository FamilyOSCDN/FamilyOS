"""Tests for plugin dependency graph nodes."""

from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def test_plugin_node_contains_plugin_package() -> None:
    package = PluginPackage(
        plugin_id="familyos.documentation",
        version="1.2.0",
        source="official",
    )

    node = PluginNode(
        package=package,
    )

    assert node.package is package


def test_plugin_node_exposes_plugin_name() -> None:
    node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )

    assert node.name == "familyos.documentation"


def test_plugin_node_exposes_plugin_version() -> None:
    node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )

    assert node.version == "1.2.0"


def test_plugin_node_identifier_uses_package_identifier() -> None:
    node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )

    assert node.identifier() == "familyos.documentation@1.2.0"


def test_plugin_nodes_are_equal_for_equal_packages() -> None:
    first_node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )
    second_node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )

    assert first_node == second_node


def test_plugin_nodes_are_different_for_different_versions() -> None:
    first_node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.0.0",
            source="official",
        ),
    )
    second_node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="2.0.0",
            source="official",
        ),
    )

    assert first_node != second_node


def test_plugin_node_is_hashable() -> None:
    node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )

    nodes = {
        node,
    }

    assert node in nodes


def test_plugin_node_is_immutable() -> None:
    node = PluginNode(
        package=PluginPackage(
            plugin_id="familyos.documentation",
            version="1.2.0",
            source="official",
        ),
    )

    assert node.package.name == "familyos.documentation"
    assert node.package.version == "1.2.0"
