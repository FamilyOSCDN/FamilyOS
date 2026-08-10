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
    def plugin_id(
        self,
    ) -> str:
        """Return the canonical plugin identifier."""

        return self.package.plugin_id

    @property
    def name(
        self,
    ) -> str:
        """Return the legacy plugin identifier alias."""

        return self.plugin_id

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
