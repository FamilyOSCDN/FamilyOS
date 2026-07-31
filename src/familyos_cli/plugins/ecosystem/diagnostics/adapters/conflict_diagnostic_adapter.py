"""Adapter from plugin conflicts to resolution diagnostics."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.conflicts import (
    ConflictReason,
    PluginConflict,
)
from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_kind import (
    DiagnosticKind,
)
from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


class ConflictDiagnosticAdapter:
    """Adapt technical plugin conflicts into user-facing diagnostics."""

    def adapt(
        self,
        conflicts: tuple[PluginConflict, ...],
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return diagnostics for the given conflicts."""

        return tuple(
            self._adapt_conflict(conflict)
            for conflict in conflicts
        )

    def _adapt_conflict(
        self,
        conflict: PluginConflict,
    ) -> PluginResolutionDiagnostic:
        """Adapt one technical conflict."""

        return PluginResolutionDiagnostic(
            kind=self._diagnostic_kind(conflict.reason),
            severity=DiagnosticSeverity.ERROR,
            message=self._message(conflict),
            plugin=conflict.plugin,
            details=self._details(conflict),
            path=(
                *conflict.required_by,
                conflict.plugin,
            ),
        )

    @staticmethod
    def _diagnostic_kind(
        reason: ConflictReason,
    ) -> DiagnosticKind:
        """Return the diagnostic kind associated with a conflict reason."""

        if reason is ConflictReason.PACKAGE_NOT_FOUND:
            return DiagnosticKind.MISSING_DEPENDENCY

        if reason is ConflictReason.INVALID_VERSION:
            return DiagnosticKind.INVALID_PACKAGE

        return DiagnosticKind.VERSION_CONFLICT

    @staticmethod
    def _message(
        conflict: PluginConflict,
    ) -> str:
        """Return a stable human-readable conflict message."""

        if conflict.reason is ConflictReason.PACKAGE_NOT_FOUND:
            return (
                f"Plugin {conflict.plugin!r} is required but not available."
            )

        if conflict.reason is ConflictReason.INVALID_VERSION:
            return (
                f"Plugin {conflict.plugin!r} has an invalid package version."
            )

        if conflict.reason is ConflictReason.INCOMPATIBLE_CONSTRAINTS:
            return (
                f"Plugin {conflict.plugin!r} has incompatible "
                "version constraints."
            )

        return (
            f"No compatible version is available for "
            f"plugin {conflict.plugin!r}."
        )

    @staticmethod
    def _details(
        conflict: PluginConflict,
    ) -> tuple[str, ...]:
        """Return structured textual details for a conflict."""

        details: list[str] = []

        details.extend(
            f"Required by: {plugin}"
            for plugin in conflict.required_by
        )
        details.extend(
            f"Requested constraint: {constraint}"
            for constraint in conflict.requested_constraints
        )
        details.extend(
            f"Available version: {version}"
            for version in conflict.available_versions
        )

        return tuple(details)
