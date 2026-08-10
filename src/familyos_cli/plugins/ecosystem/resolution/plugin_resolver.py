"""Plugin dependency resolver."""

from __future__ import annotations

from collections import defaultdict

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_package_selector import (
    PluginPackageSelector,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_plan import (
    ResolutionPlan,
)


class PluginResolver:
    """Resolve plugin dependencies against available packages."""

    def __init__(
        self,
        package_selector: PluginPackageSelector | None = None,
    ) -> None:
        """Initialize the plugin resolver."""

        self._package_selector = (
            package_selector
            if package_selector is not None
            else PluginPackageSelector()
        )

    def resolve(
        self,
        dependencies: list[PluginDependency],
        available_packages: list[PluginPackage],
    ) -> ResolutionPlan:
        """Resolve dependencies against available plugin packages."""

        ordered_packages: list[PluginPackage] = []
        skipped_packages: list[PluginPackage] = []
        diagnostics: list[ResolutionDiagnostic] = []

        packages_by_plugin_id = self._group_packages_by_plugin_id(
            available_packages,
        )

        for dependency in dependencies:
            candidates = packages_by_plugin_id.get(
                dependency.plugin_id,
                [],
            )

            if not candidates:
                diagnostics.append(
                    ResolutionDiagnostic(
                        plugin=dependency.plugin_id,
                        message=(
                            "Required plugin dependency is not available."
                        ),
                    ),
                )
                continue

            selected_package = self._package_selector.select(
                dependency=dependency,
                candidates=candidates,
            )

            self._collect_candidate_outcomes(
                dependency=dependency,
                candidates=candidates,
                skipped_packages=skipped_packages,
                diagnostics=diagnostics,
            )

            if selected_package is None:
                diagnostics.append(
                    ResolutionDiagnostic(
                        plugin=dependency.plugin_id,
                        message=self._build_incompatibility_message(
                            dependency,
                        ),
                    ),
                )
                continue

            ordered_packages.append(
                selected_package,
            )

        return ResolutionPlan(
            ordered_packages=ordered_packages,
            skipped_packages=skipped_packages,
            diagnostics=diagnostics,
        )

    @staticmethod
    def _group_packages_by_plugin_id(
        available_packages: list[PluginPackage],
    ) -> dict[str, list[PluginPackage]]:
        """Group available packages by Plugin Identifier."""

        packages_by_plugin_id: defaultdict[
            str,
            list[PluginPackage],
        ] = defaultdict(list)

        for package in available_packages:
            packages_by_plugin_id[package.plugin_id].append(
                package,
            )

        return dict(
            packages_by_plugin_id,
        )

    @staticmethod
    def _collect_candidate_outcomes(
        *,
        dependency: PluginDependency,
        candidates: list[PluginPackage],
        skipped_packages: list[PluginPackage],
        diagnostics: list[ResolutionDiagnostic],
    ) -> None:
        """Collect invalid and incompatible candidate outcomes.

        Valid compatible candidates are not considered skipped, even when
        another compatible candidate has a higher version.
        """

        for package in candidates:
            try:
                package_version = PluginVersion.parse(
                    package.version,
                )
            except ValueError:
                skipped_packages.append(
                    package,
                )
                diagnostics.append(
                    ResolutionDiagnostic(
                        plugin=dependency.plugin_id,
                        message=(
                            f"Plugin package version {package.version!r} "
                            "is invalid."
                        ),
                    ),
                )
                continue

            if (
                dependency.constraint_set is not None
                and not dependency.constraint_set.is_satisfied_by(
                    package_version,
                )
            ):
                skipped_packages.append(
                    package,
                )

    @staticmethod
    def _build_incompatibility_message(
        dependency: PluginDependency,
    ) -> str:
        """Build the diagnostic for an unresolved dependency."""

        if dependency.constraint_set is None:
            return (
                "No package with a valid semantic version is available."
            )

        return (
            "No available plugin version satisfies constraint set "
            f"{str(dependency.constraint_set)!r}."
        )
