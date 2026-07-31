"""Plugin dependency graph."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.dependency_graph.dependency_edge import (
    DependencyEdge,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)


@dataclass(slots=True)
class PluginDependencyGraph:
    """Represent a directed plugin dependency graph."""

    _nodes: dict[str, PluginNode] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _edges: set[DependencyEdge] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    def add_node(
        self,
        node: PluginNode,
    ) -> None:
        """Add a node to the graph."""

        self._nodes.setdefault(
            node.identifier(),
            node,
        )

    def add_edge(
        self,
        edge: DependencyEdge,
    ) -> None:
        """Add a dependency edge."""

        self.add_node(
            edge.source,
        )
        self.add_node(
            edge.target,
        )

        self._edges.add(
            edge,
        )

    @property
    def nodes(
        self,
    ) -> tuple[PluginNode, ...]:
        """Return all graph nodes."""

        return tuple(
            self._nodes.values(),
        )

    @property
    def edges(
        self,
    ) -> tuple[DependencyEdge, ...]:
        """Return all dependency edges."""

        return tuple(
            self._edges,
        )

    def contains(
        self,
        node: PluginNode,
    ) -> bool:
        """Return whether a node belongs to the graph."""

        return (
            node.identifier()
            in self._nodes
        )

    def outgoing_edges(
        self,
        node: PluginNode,
    ) -> tuple[DependencyEdge, ...]:
        """Return outgoing edges of a node."""

        return tuple(
            edge
            for edge in self._edges
            if edge.source == node
        )

    def incoming_edges(
        self,
        node: PluginNode,
    ) -> tuple[DependencyEdge, ...]:
        """Return incoming edges of a node."""

        return tuple(
            edge
            for edge in self._edges
            if edge.target == node
        )
