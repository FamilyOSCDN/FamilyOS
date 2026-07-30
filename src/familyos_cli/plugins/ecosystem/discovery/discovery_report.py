"""Plugin discovery report."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)


@dataclass(frozen=True, slots=True)
class PluginDiscoveryReport:
    """Result of a plugin discovery operation."""

    repository: PluginRepository

    packages: tuple[PluginPackage, ...]

    warnings: tuple[str, ...] = ()

    errors: tuple[str, ...] = ()

    @property
    def package_count(
        self,
    ) -> int:
        """Return number of discovered packages."""

        return len(self.packages)

    @property
    def has_warnings(
        self,
    ) -> bool:
        """Return whether warnings were produced."""

        return bool(self.warnings)

    @property
    def has_errors(
        self,
    ) -> bool:
        """Return whether errors were produced."""

        return bool(self.errors)

    @property
    def successful(
        self,
    ) -> bool:
        """Return whether discovery completed successfully."""

        return not self.has_errors
