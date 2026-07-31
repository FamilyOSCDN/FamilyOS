"""Plugin dependency graph cycle detection."""

from __future__ import annotations

from enum import Enum, auto

from familyos_cli.plugins.ecosystem.dependency_graph.plugin_dependency_graph import (
    PluginDependencyGraph,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)


class _VisitState(Enum):
    """Represent the traversal state of a graph node."""

    VISITING = auto()
    VISITED = auto()


class CycleDetector:
    """Detect cycles in a plugin dependency graph."""

    def has_cycle(
        self,
        graph: PluginDependencyGraph,
    ) -> bool:
        """Return whether the dependency graph contains a cycle."""

        states: dict[PluginNode, _VisitState] = {}

        for node in graph.nodes:
            if node in states:
                continue

            if self._has_cycle_from(
                graph=graph,
                node=node,
                states=states,
            ):
                return True

        return False

    def _has_cycle_from(
        self,
        graph: PluginDependencyGraph,
        node: PluginNode,
        states: dict[PluginNode, _VisitState],
    ) -> bool:
        """Return whether a cycle is reachable from a node."""

        state = states.get(
            node,
        )

        if state is _VisitState.VISITING:
            return True

        if state is _VisitState.VISITED:
            return False

        states[node] = _VisitState.VISITING

        for edge in graph.outgoing_edges(
            node,
        ):
            if self._has_cycle_from(
                graph=graph,
                node=edge.target,
                states=states,
            ):
                return True

        states[node] = _VisitState.VISITED

        return False
