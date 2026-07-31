"""Plugin dependency cycle detector."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.cycles import (
    DependencyCycle,
)
from familyos_cli.plugins.ecosystem.diagnostics.ports import (
    CycleDetectionSource,
)


class CycleDetector:
    """Detect cycles in plugin dependency graphs."""

    def __init__(
        self,
        source: CycleDetectionSource,
    ) -> None:
        """Initialize the detector."""

        self._source = source

    def detect(self) -> tuple[DependencyCycle, ...]:
        """Detect all dependency cycles."""

        cycles: list[DependencyCycle] = []
        visited: set[str] = set()
        active: list[str] = []

        for plugin in self._source.plugins():
            self._visit(
                plugin=plugin,
                visited=visited,
                active=active,
                cycles=cycles,
            )

        return tuple(
            cycles,
        )

    def _visit(
        self,
        *,
        plugin: str,
        visited: set[str],
        active: list[str],
        cycles: list[DependencyCycle],
    ) -> None:
        """Visit a dependency node using depth-first traversal."""

        if plugin in active:
            cycle_start = active.index(
                plugin,
            )

            cycle = DependencyCycle(
                path=(
                    *active[cycle_start:],
                    plugin,
                ),
            ).normalized()

            if cycle not in cycles:
                cycles.append(
                    cycle,
                )

            return

        if plugin in visited:
            return

        active.append(
            plugin,
        )

        for dependency in self._source.dependencies_of(
            plugin,
        ):
            self._visit(
                plugin=dependency,
                visited=visited,
                active=active,
                cycles=cycles,
            )

        active.pop()

        visited.add(
            plugin,
        )
