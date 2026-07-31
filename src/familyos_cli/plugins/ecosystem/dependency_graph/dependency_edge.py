"""Dependency graph edge."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    """Represent a directed dependency between two plugin nodes."""

    source: PluginNode
    target: PluginNode
    dependency: PluginDependency | None = None

    def __post_init__(
        self,
    ) -> None:
        """Validate dependency edge consistency."""

        if (
            self.dependency is not None
            and self.dependency.name != self.target.name
        ):
            raise ValueError(
                "Dependency edge requirement must reference "
                f"target plugin {self.target.name!r}.",
            )

    def identifier(
        self,
    ) -> str:
        """Return a stable edge identifier."""

        return (
            f"{self.source.identifier()}"
            f"->{self.target.identifier()}"
        )
