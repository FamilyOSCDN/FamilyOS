"""Plugin installation service."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.installation.installed_plugin import (
    InstalledPlugin,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


class PluginInstaller:
    """Install verified plugin packages."""

    def install(
        self,
        package: PluginPackage,
        location: str,
    ) -> InstalledPlugin:
        """Create installed plugin representation."""

        return InstalledPlugin(
            name=package.name,
            version=package.version,
            location=location,
        )
