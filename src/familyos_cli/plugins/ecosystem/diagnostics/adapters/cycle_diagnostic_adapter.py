"""Adapter from dependency cycles to resolution diagnostics."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.cycles import (
    DependencyCycle,
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


class CycleDiagnosticAdapter:
    """Convert dependency cycles into resolution diagnostics."""

    def adapt(
        self,
        cycles: tuple[DependencyCycle, ...],
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return diagnostics generated from dependency cycles."""

        return tuple(
            self._adapt_cycle(cycle)
            for cycle in cycles
        )

    @staticmethod
    def _adapt_cycle(
        cycle: DependencyCycle,
    ) -> PluginResolutionDiagnostic:
        """Convert one dependency cycle into a diagnostic."""

        return PluginResolutionDiagnostic(
            kind=DiagnosticKind.DEPENDENCY_CYCLE,
            severity=DiagnosticSeverity.ERROR,
            message=(
                "Plugin dependency cycle detected."
            ),
            plugin=cycle.plugin,
            path=cycle.path,
            details=(
                "Dependency path: "
                + " -> ".join(cycle.path),
            ),
        )
