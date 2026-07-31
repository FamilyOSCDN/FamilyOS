"""Tests for the plugin dependency graph builder."""

from collections.abc import Sequence

from familyos_cli.plugins.ecosystem.dependency_graph import (
    DependencyGraphBuilder,
    PluginDependencyGraph,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginManifest,
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
    PluginPackageSelector,
)


class RecordingPluginPackageSelector(
    PluginPackageSelector,
):
    """Record package selector calls for builder tests."""

    def __init__(
        self,
        selected_package: PluginPackage | None,
    ) -> None:
        """Initialize the recording selector."""

        self.selected_package = selected_package
        self.calls: list[
            tuple[
                PluginDependency,
                tuple[PluginPackage, ...],
            ]
        ] = []

    def select(
        self,
        dependency: PluginDependency,
        candidates: Sequence[PluginPackage],
    ) -> PluginPackage | None:
        """Record the selection request and return configured result."""

        self.calls.append(
            (
                dependency,
                tuple(candidates),
            ),
        )

        return self.selected_package


def test_build_empty_graph() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (),
    )

    assert graph.nodes == ()
    assert graph.edges == ()


def test_build_single_node() -> None:
    builder = DependencyGraphBuilder()

    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.0.0",
            source="official",
        ),
    )

    graph = builder.build(
        (
            manifest,
        ),
    )

    assert len(graph.nodes) == 1
    assert graph.nodes[0].identifier() == "calendar@1.0.0"
    assert graph.edges == ()


def test_build_multiple_nodes() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="storage",
                    version="3.1.0",
                    source="official",
                ),
            ),
        ),
    )

    node_identifiers = {
        node.identifier()
        for node in graph.nodes
    }

    assert node_identifiers == {
        "calendar@1.0.0",
        "identity@2.0.0",
        "storage@3.1.0",
    }
    assert graph.edges == ()


def test_build_keeps_multiple_versions_of_same_plugin() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="1.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
            ),
        ),
    )

    node_identifiers = {
        node.identifier()
        for node in graph.nodes
    }

    assert node_identifiers == {
        "identity@1.0.0",
        "identity@2.0.0",
    }


def test_duplicate_manifest_is_ignored() -> None:
    builder = DependencyGraphBuilder()

    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.0.0",
            source="official",
        ),
    )

    graph = builder.build(
        (
            manifest,
            manifest,
        ),
    )

    assert len(graph.nodes) == 1
    assert graph.nodes[0].identifier() == "calendar@1.0.0"


def test_build_node_index_groups_nodes_by_name() -> None:
    builder = DependencyGraphBuilder()

    manifests = (
        PluginManifest(
            package=PluginPackage(
                name="calendar",
                version="1.0.0",
                source="official",
            ),
        ),
        PluginManifest(
            package=PluginPackage(
                name="identity",
                version="2.0.0",
                source="official",
            ),
        ),
    )

    graph = PluginDependencyGraph()

    node_index = builder._build_node_index(
        manifests=manifests,
        graph=graph,
    )

    assert set(node_index) == {
        "calendar",
        "identity",
    }

    assert [
        node.identifier()
        for node in node_index["calendar"]
    ] == [
        "calendar@1.0.0",
    ]

    assert [
        node.identifier()
        for node in node_index["identity"]
    ] == [
        "identity@2.0.0",
    ]


def test_build_node_index_groups_multiple_versions() -> None:
    builder = DependencyGraphBuilder()

    manifests = (
        PluginManifest(
            package=PluginPackage(
                name="identity",
                version="1.0.0",
                source="official",
            ),
        ),
        PluginManifest(
            package=PluginPackage(
                name="identity",
                version="2.0.0",
                source="official",
            ),
        ),
        PluginManifest(
            package=PluginPackage(
                name="identity",
                version="2.1.0",
                source="official",
            ),
        ),
    )

    graph = PluginDependencyGraph()

    node_index = builder._build_node_index(
        manifests=manifests,
        graph=graph,
    )

    assert set(node_index) == {
        "identity",
    }

    assert {
        node.identifier()
        for node in node_index["identity"]
    } == {
        "identity@1.0.0",
        "identity@2.0.0",
        "identity@2.1.0",
    }


def test_build_node_index_populates_graph() -> None:
    builder = DependencyGraphBuilder()

    manifests = (
        PluginManifest(
            package=PluginPackage(
                name="calendar",
                version="1.0.0",
                source="official",
            ),
        ),
    )

    graph = PluginDependencyGraph()

    node_index = builder._build_node_index(
        manifests=manifests,
        graph=graph,
    )

    assert len(graph.nodes) == 1
    assert graph.nodes[0] == node_index["calendar"][0]


def test_build_node_index_ignores_duplicate_manifest() -> None:
    builder = DependencyGraphBuilder()

    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.0.0",
            source="official",
        ),
    )

    graph = PluginDependencyGraph()

    node_index = builder._build_node_index(
        manifests=(
            manifest,
            manifest,
        ),
        graph=graph,
    )

    assert len(graph.nodes) == 1
    assert len(node_index["calendar"]) == 1
    assert (
        node_index["calendar"][0].identifier()
        == "calendar@1.0.0"
    )


def test_build_creates_dependency_edge() -> None:
    builder = DependencyGraphBuilder()

    calendar_manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.0.0",
            source="official",
        ),
        dependencies=(
            PluginDependency(
                name="identity",
            ),
        ),
    )
    identity_manifest = PluginManifest(
        package=PluginPackage(
            name="identity",
            version="2.0.0",
            source="official",
        ),
    )

    graph = builder.build(
        (
            calendar_manifest,
            identity_manifest,
        ),
    )

    assert len(graph.edges) == 1

    edge = graph.edges[0]

    assert edge.source.identifier() == "calendar@1.0.0"
    assert edge.target.identifier() == "identity@2.0.0"
    assert edge.dependency == calendar_manifest.dependencies[0]


def test_build_creates_multiple_dependency_edges() -> None:
    builder = DependencyGraphBuilder()

    calendar_manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.0.0",
            source="official",
        ),
        dependencies=(
            PluginDependency(
                name="identity",
            ),
            PluginDependency(
                name="storage",
            ),
        ),
    )

    graph = builder.build(
        (
            calendar_manifest,
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="storage",
                    version="3.0.0",
                    source="official",
                ),
            ),
        ),
    )

    edge_identifiers = {
        edge.identifier()
        for edge in graph.edges
    }

    assert edge_identifiers == {
        "calendar@1.0.0->identity@2.0.0",
        "calendar@1.0.0->storage@3.0.0",
    }


def test_build_selects_highest_available_dependency_version() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="identity",
                    ),
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="1.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.1.0",
                    source="official",
                ),
            ),
        ),
    )

    assert len(graph.edges) == 1
    assert (
        graph.edges[0].target.identifier()
        == "identity@2.1.0"
    )


def test_build_selects_highest_compatible_dependency_version() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="identity",
                        minimum_version="2.0.0",
                    ),
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="1.5.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.2.0",
                    source="official",
                ),
            ),
        ),
    )

    assert len(graph.edges) == 1
    assert (
        graph.edges[0].target.identifier()
        == "identity@2.2.0"
    )


def test_build_ignores_dependency_without_available_package() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="identity",
                    ),
                ),
            ),
        ),
    )

    assert len(graph.nodes) == 1
    assert graph.edges == ()


def test_build_ignores_incompatible_dependency_versions() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="identity",
                        minimum_version="3.0.0",
                    ),
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="1.0.0",
                    source="official",
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
            ),
        ),
    )

    assert graph.edges == ()


def test_build_ignores_invalid_dependency_package_version() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="identity",
                    ),
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="invalid",
                    source="official",
                ),
            ),
        ),
    )

    assert len(graph.nodes) == 2
    assert graph.edges == ()


def test_build_supports_transitive_dependency_edges() -> None:
    builder = DependencyGraphBuilder()

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="identity",
                    ),
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="2.0.0",
                    source="official",
                ),
                dependencies=(
                    PluginDependency(
                        name="storage",
                    ),
                ),
            ),
            PluginManifest(
                package=PluginPackage(
                    name="storage",
                    version="3.0.0",
                    source="official",
                ),
            ),
        ),
    )

    edge_identifiers = {
        edge.identifier()
        for edge in graph.edges
    }

    assert edge_identifiers == {
        "calendar@1.0.0->identity@2.0.0",
        "identity@2.0.0->storage@3.0.0",
    }


def test_build_delegates_selection_to_package_selector() -> None:
    identity_package = PluginPackage(
        name="identity",
        version="2.0.0",
        source="official",
    )
    dependency = PluginDependency(
        name="identity",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=identity_package,
    )
    builder = DependencyGraphBuilder(
        package_selector=selector,
    )

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    dependency,
                ),
            ),
            PluginManifest(
                package=identity_package,
            ),
        ),
    )

    assert selector.calls == [
        (
            dependency,
            (
                identity_package,
            ),
        ),
    ]
    assert len(graph.edges) == 1
    assert (
        graph.edges[0].target.package
        == identity_package
    )


def test_build_skips_edge_when_selector_returns_none() -> None:
    dependency = PluginDependency(
        name="identity",
    )
    identity_package = PluginPackage(
        name="identity",
        version="2.0.0",
        source="official",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=None,
    )
    builder = DependencyGraphBuilder(
        package_selector=selector,
    )

    graph = builder.build(
        (
            PluginManifest(
                package=PluginPackage(
                    name="calendar",
                    version="1.0.0",
                    source="official",
                ),
                dependencies=(
                    dependency,
                ),
            ),
            PluginManifest(
                package=identity_package,
            ),
        ),
    )

    assert selector.calls == [
        (
            dependency,
            (
                identity_package,
            ),
        ),
    ]
    assert graph.edges == ()


def test_find_node_for_package_returns_matching_node() -> None:
    package = PluginPackage(
        name="identity",
        version="2.0.0",
        source="official",
    )
    builder = DependencyGraphBuilder()
    graph = PluginDependencyGraph()

    node_index = builder._build_node_index(
        manifests=(
            PluginManifest(
                package=package,
            ),
        ),
        graph=graph,
    )

    selected_node = builder._find_node_for_package(
        package=package,
        candidates=node_index["identity"],
    )

    assert selected_node is not None
    assert selected_node.package == package


def test_find_node_for_package_returns_none_when_absent() -> None:
    builder = DependencyGraphBuilder()
    graph = PluginDependencyGraph()

    node_index = builder._build_node_index(
        manifests=(
            PluginManifest(
                package=PluginPackage(
                    name="identity",
                    version="1.0.0",
                    source="official",
                ),
            ),
        ),
        graph=graph,
    )

    selected_node = builder._find_node_for_package(
        package=PluginPackage(
            name="identity",
            version="2.0.0",
            source="official",
        ),
        candidates=node_index["identity"],
    )

    assert selected_node is None
