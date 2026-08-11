"""Plugin dependency graph resolver."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.dependency_graph.cycle_detector import (
    CycleDetector,
)
from familyos_cli.plugins.ecosystem.dependency_graph.dependency_resolution_result import (
    DependencyResolutionResult,
)
from familyos_cli.plugins.ecosystem.dependency_graph.plugin_dependency_graph import (
    PluginDependencyGraph,
)
from familyos_cli.plugins.ecosystem.dependency_graph.topological_sorter import (
    TopologicalSorter,
)


class DependencyGraphResolver:
    """Resolve plugin dependency graphs into dependency-first order."""

    def __init__(
        self,
        cycle_detector: CycleDetector | None = None,
        topological_sorter: TopologicalSorter | None = None,
    ) -> None:
        """Initialize the dependency graph resolver."""

        self._cycle_detector = (
            cycle_detector if cycle_detector is not None else CycleDetector()
        )
        self._topological_sorter = (
            topological_sorter
            if topological_sorter is not None
            else TopologicalSorter()
        )

    def resolve(
        self,
        graph: PluginDependencyGraph,
    ) -> DependencyResolutionResult:
        """Resolve a plugin dependency graph."""

        if self._cycle_detector.has_cycle(
            graph,
        ):
            return DependencyResolutionResult.cyclic()

        ordered_nodes = self._topological_sorter.sort(
            graph,
        )

        return DependencyResolutionResult.resolved(
            ordered_nodes,
        )
