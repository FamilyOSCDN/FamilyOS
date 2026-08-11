"""Plugin dependency graph topological sorting."""

from __future__ import annotations

import heapq

from familyos_cli.plugins.ecosystem.dependency_graph.plugin_dependency_graph import (
    PluginDependencyGraph,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)


class TopologicalSorter:
    """Produce a dependency-first ordering of plugin graph nodes."""

    def sort(
        self,
        graph: PluginDependencyGraph,
    ) -> tuple[PluginNode, ...]:
        """Return graph nodes in dependency-first order.

        When an edge points from a plugin to one of its dependencies, the
        dependency is placed before the dependent plugin.

        Args:
            graph: Plugin dependency graph to sort.

        Returns:
            Nodes ordered so every dependency precedes its dependents.

        Raises:
            ValueError: If the graph contains a dependency cycle.
        """

        remaining_dependencies = {
            node: len(
                graph.outgoing_edges(
                    node,
                ),
            )
            for node in graph.nodes
        }

        ready_nodes: list[tuple[str, PluginNode]] = [
            (
                node.identifier(),
                node,
            )
            for node, dependency_count in remaining_dependencies.items()
            if dependency_count == 0
        ]

        heapq.heapify(
            ready_nodes,
        )

        ordered_nodes: list[PluginNode] = []

        while ready_nodes:
            _, node = heapq.heappop(
                ready_nodes,
            )

            ordered_nodes.append(
                node,
            )

            dependent_edges = sorted(
                graph.incoming_edges(
                    node,
                ),
                key=lambda edge: edge.source.identifier(),
            )

            for edge in dependent_edges:
                dependent = edge.source

                remaining_dependencies[dependent] -= 1

                if remaining_dependencies[dependent] == 0:
                    heapq.heappush(
                        ready_nodes,
                        (
                            dependent.identifier(),
                            dependent,
                        ),
                    )

        if len(ordered_nodes) != len(graph.nodes):
            raise ValueError(
                "Cannot topologically sort a dependency graph containing a cycle.",
            )

        return tuple(
            ordered_nodes,
        )
