"""Plugin discovery service."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.plugins import (
    PluginDiscoveryPort,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)
from familyos_cli.plugins.plugin_loader import (
    PluginLoader,
)


class PluginDiscovery(PluginDiscoveryPort):
    """Discover available plugins from repositories."""

    def __init__(
        self,
        loader: PluginLoader | None = None,
    ) -> None:
        """Initialize plugin discovery.

        Args:
            loader: Plugin descriptor loader.
        """

        self._loader = loader or PluginLoader()

    def discover(
        self,
        repository: PluginRepository,
    ) -> list[PluginPackage]:
        """Discover plugins from a repository.

        Args:
            repository: Plugin source.

        Returns:
            Available plugin packages.
        """

        if not repository.enabled:
            return []

        if repository.repository_type != "local":
            return []

        descriptors = self._loader.discover(
            Path(repository.url),
        )

        return [
            PluginPackage(
                name=descriptor.name,
                version=descriptor.version,
                source=repository.name,
            )
            for descriptor in descriptors
            if descriptor.enabled
        ]
