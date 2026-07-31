"""Plugin dependency graph node."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


@dataclass(frozen=True, slots=True)
class PluginNode:
    """Represent a plugin package inside a dependency graph."""

    package: PluginPackage

    @property
    def name(
        self,
    ) -> str:
        """Return the plugin name."""

        return self.package.name

    @property
    def version(
        self,
    ) -> str:
        """Return the plugin version."""

        return self.package.version

    def identifier(
        self,
    ) -> str:
        """Return the unique graph node identifier."""

        return self.package.identifier()
