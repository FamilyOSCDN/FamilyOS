"""Plugin installer port."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.plugins.ecosystem.installation import (
    InstalledPlugin,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


class PluginInstallerPort(ABC):
    """Contract for plugin installation."""

    @abstractmethod
    def install(
        self,
        package: PluginPackage,
        location: str,
    ) -> InstalledPlugin:
        """Install a plugin package."""

        raise NotImplementedError
