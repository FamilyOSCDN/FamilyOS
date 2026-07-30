"""Plugin dependency resolver."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_plan import (
    ResolutionPlan,
)


class PluginResolver:
    """Resolve plugin dependencies against available packages."""

    def resolve(
        self,
        dependencies: list[PluginDependency],
        available_packages: list[PluginPackage],
    ) -> ResolutionPlan:
        """Resolve dependencies against available plugin packages.

        Args:
            dependencies: Plugin dependency requirements.
            available_packages: Packages available for resolution.

        Returns:
            A structured resolution plan.
        """

        ordered_packages: list[PluginPackage] = []
        diagnostics: list[ResolutionDiagnostic] = []

        packages_by_name = {
            package.name: package
            for package in available_packages
        }

        for dependency in dependencies:
            package = packages_by_name.get(dependency.name)

            if package is None:
                diagnostics.append(
                    ResolutionDiagnostic(
                        plugin=dependency.name,
                        message=(
                            "Required plugin dependency is not available."
                        ),
                    ),
                )
                continue

            ordered_packages.append(package)

        return ResolutionPlan(
            ordered_packages=ordered_packages,
            diagnostics=diagnostics,
        )
