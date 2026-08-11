"""Plugin dependency graph builder."""

from __future__ import annotations

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
    PluginManifest,
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_package_selector import (
    PluginPackageSelector,
)


class DependencyGraphBuilder:
    """Build plugin dependency graphs from plugin manifests."""

    def __init__(
        self,
        package_selector: PluginPackageSelector | None = None,
    ) -> None:
        """Initialize the dependency graph builder."""

        self._package_selector = (
            package_selector
            if package_selector is not None
            else PluginPackageSelector()
        )

    def build(
        self,
        manifests: tuple[PluginManifest, ...],
    ) -> PluginDependencyGraph:
        """Build a dependency graph from plugin manifests."""

        graph = PluginDependencyGraph()

        node_index = self._build_node_index(
            manifests=manifests,
            graph=graph,
        )

        self._build_edges(
            manifests=manifests,
            node_index=node_index,
            graph=graph,
        )

        return graph

    def _build_node_index(
        self,
        *,
        manifests: tuple[PluginManifest, ...],
        graph: PluginDependencyGraph,
    ) -> dict[str, list[PluginNode]]:
        """Create graph nodes indexed by Plugin Identifier."""

        node_index: dict[
            str,
            list[PluginNode],
        ] = {}

        for manifest in manifests:
            node = PluginNode(
                package=manifest.package,
            )

            graph.add_node(
                node,
            )

            nodes_by_plugin_id = node_index.setdefault(
                node.plugin_id,
                [],
            )

            if node not in nodes_by_plugin_id:
                nodes_by_plugin_id.append(
                    node,
                )

        return node_index

    def _build_edges(
        self,
        *,
        manifests: tuple[PluginManifest, ...],
        node_index: dict[str, list[PluginNode]],
        graph: PluginDependencyGraph,
    ) -> None:
        """Create dependency edges between compatible plugin nodes."""

        for manifest in manifests:
            source_node = self._find_source_node(
                manifest=manifest,
                node_index=node_index,
            )

            if source_node is None:
                continue

            for dependency in manifest.dependencies:
                target_node = self._select_dependency_node(
                    dependency=dependency,
                    node_index=node_index,
                )

                if target_node is None:
                    continue

                graph.add_edge(
                    DependencyEdge(
                        source=source_node,
                        target=target_node,
                        dependency=dependency,
                    ),
                )

    @staticmethod
    def _find_source_node(
        *,
        manifest: PluginManifest,
        node_index: dict[str, list[PluginNode]],
    ) -> PluginNode | None:
        """Return the node representing a manifest package."""

        candidates = node_index.get(
            manifest.package.plugin_id,
            [],
        )

        for candidate in candidates:
            if candidate.package == manifest.package:
                return candidate

        return None

    def _select_dependency_node(
        self,
        *,
        dependency: PluginDependency,
        node_index: dict[str, list[PluginNode]],
    ) -> PluginNode | None:
        """Select the node carrying the highest compatible package."""

        candidates = node_index.get(
            dependency.plugin_id,
            [],
        )

        packages = tuple(node.package for node in candidates)

        selected_package = self._package_selector.select(
            dependency=dependency,
            candidates=packages,
        )

        if selected_package is None:
            return None

        return self._find_node_for_package(
            package=selected_package,
            candidates=candidates,
        )

    @staticmethod
    def _find_node_for_package(
        *,
        package: PluginPackage,
        candidates: list[PluginNode],
    ) -> PluginNode | None:
        """Return the node carrying a selected package."""

        for candidate in candidates:
            if candidate.package == package:
                return candidate

        return None
