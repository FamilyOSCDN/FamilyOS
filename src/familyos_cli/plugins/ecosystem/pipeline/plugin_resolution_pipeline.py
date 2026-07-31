"""Plugin resolution pipeline."""

from __future__ import annotations

from familyos_cli.application.ports.plugins import (
    PluginDiscoveryPort,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
    PluginResolver,
    ResolutionPlan,
)


class PluginResolutionPipeline:
    """Coordinate plugin discovery and dependency resolution."""

    def __init__(
        self,
        discovery: PluginDiscoveryPort,
        resolver: PluginResolver,
    ) -> None:
        """Initialize the pipeline."""

        self._discovery = discovery
        self._resolver = resolver

    def resolve(
        self,
        repository: PluginRepository,
        dependencies: list[PluginDependency],
    ) -> ResolutionPlan:
        """Resolve plugin dependencies from a repository."""

        packages = self._discovery.discover(
            repository,
        )

        return self._resolver.resolve(
            dependencies,
            packages,
        )
