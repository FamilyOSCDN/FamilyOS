"""Plugin package selection service."""

from __future__ import annotations

from collections.abc import Sequence

from familyos_cli.plugins.ecosystem.package.plugin_package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)


class PluginPackageSelector:
    """Select the highest compatible plugin package."""

    def select(
        self,
        dependency: PluginDependency,
        candidates: Sequence[PluginPackage],
    ) -> PluginPackage | None:
        """Select the highest compatible package.

        Packages with invalid semantic versions are ignored. When the
        dependency has a constraint set, only packages satisfying all
        constraints are considered.

        Args:
            dependency: Plugin dependency requirement.
            candidates: Available packages for the required plugin.

        Returns:
            Highest compatible package, or ``None`` when no compatible
            package is available.
        """

        compatible_packages: list[
            tuple[PluginPackage, PluginVersion]
        ] = []

        for candidate in candidates:
            package_version = self._parse_version(
                candidate,
            )

            if package_version is None:
                continue

            if not self._is_compatible(
                dependency=dependency,
                version=package_version,
            ):
                continue

            compatible_packages.append(
                (
                    candidate,
                    package_version,
                ),
            )

        if not compatible_packages:
            return None

        return max(
            compatible_packages,
            key=lambda item: item[1],
        )[0]

    @staticmethod
    def _parse_version(
        package: PluginPackage,
    ) -> PluginVersion | None:
        """Parse a package semantic version when valid."""

        try:
            return PluginVersion.parse(
                package.version,
            )
        except ValueError:
            return None

    @staticmethod
    def _is_compatible(
        *,
        dependency: PluginDependency,
        version: PluginVersion,
    ) -> bool:
        """Return whether a version satisfies a dependency."""

        if dependency.constraint_set is None:
            return True

        return dependency.constraint_set.is_satisfied_by(
            version,
        )
