"""Plugin manifest model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from familyos_cli.plugins.ecosystem.package.plugin_package import (
    PluginPackage,
)

if TYPE_CHECKING:
    from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
        PluginDependency,
    )


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Associate a distributable plugin package with its dependencies."""

    package: PluginPackage

    dependencies: tuple[PluginDependency, ...] = field(
        default_factory=tuple,
    )

    @property
    def name(
        self,
    ) -> str:
        """Return the plugin package name."""

        return self.package.name

    @property
    def version(
        self,
    ) -> str:
        """Return the plugin package version."""

        return self.package.version

    def identifier(
        self,
    ) -> str:
        """Return the unique manifest identifier."""

        return self.package.identifier()
