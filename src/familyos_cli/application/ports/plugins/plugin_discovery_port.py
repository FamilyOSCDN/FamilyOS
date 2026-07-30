"""Plugin discovery port."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)


class PluginDiscoveryPort(ABC):
    """Contract for plugin discovery."""

    @abstractmethod
    def discover(
        self,
        repository: PluginRepository,
    ) -> list[PluginPackage]:
        """Discover available plugins."""

        raise NotImplementedError
