"""Adapter from resolution plans to plugin conflicts."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.conflicts import (
    ConflictReason,
    PluginConflict,
)
from familyos_cli.plugins.ecosystem.resolution import (
    ResolutionDiagnostic,
    ResolutionPlan,
)

_MISSING_DEPENDENCY_MESSAGE = (
    "Required plugin dependency is not available."
)
_NO_VALID_VERSION_MESSAGE = (
    "No package with a valid semantic version is available."
)
_NO_COMPATIBLE_VERSION_PREFIX = (
    "No available plugin version satisfies constraint set "
)
_INVALID_VERSION_FRAGMENT = "is invalid."


class ResolutionConflictAdapter:
    """Adapt resolver diagnostics into technical plugin conflicts."""

    def adapt(
        self,
        plan: ResolutionPlan,
    ) -> tuple[PluginConflict, ...]:
        """Return conflicts represented by a resolution plan."""

        conflicts: list[PluginConflict] = []

        for diagnostic in plan.diagnostics:
            conflict = self._adapt_diagnostic(
                diagnostic=diagnostic,
                plan=plan,
            )

            if conflict is not None:
                conflicts.append(
                    conflict,
                )

        return tuple(conflicts)

    def _adapt_diagnostic(
        self,
        *,
        diagnostic: ResolutionDiagnostic,
        plan: ResolutionPlan,
    ) -> PluginConflict | None:
        """Adapt one known resolver diagnostic."""

        message = diagnostic.message

        if message == _MISSING_DEPENDENCY_MESSAGE:
            return PluginConflict(
                plugin=diagnostic.plugin,
                reason=ConflictReason.PACKAGE_NOT_FOUND,
            )

        if _INVALID_VERSION_FRAGMENT in message:
            return PluginConflict(
                plugin=diagnostic.plugin,
                reason=ConflictReason.INVALID_VERSION,
                available_versions=self._skipped_versions_for(
                    plugin=diagnostic.plugin,
                    plan=plan,
                ),
            )

        if (
            message == _NO_VALID_VERSION_MESSAGE
            or message.startswith(
                _NO_COMPATIBLE_VERSION_PREFIX,
            )
        ):
            return PluginConflict(
                plugin=diagnostic.plugin,
                reason=ConflictReason.NO_COMPATIBLE_VERSION,
                available_versions=self._skipped_versions_for(
                    plugin=diagnostic.plugin,
                    plan=plan,
                ),
            )

        return None

    @staticmethod
    def _skipped_versions_for(
        *,
        plugin: str,
        plan: ResolutionPlan,
    ) -> tuple[str, ...]:
        """Return unique skipped versions for a plugin in plan order."""

        versions: list[str] = []

        for package in plan.skipped_packages:
            if package.plugin_id != plugin:
                continue

            if package.version not in versions:
                versions.append(
                    package.version,
                )

        return tuple(versions)
