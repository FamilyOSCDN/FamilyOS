"""Resolution-plan adapter producing conflict diagnostics."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.adapters.conflict_diagnostic_adapter import (
    ConflictDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.diagnostics.adapters.resolution_conflict_adapter import (
    ResolutionConflictAdapter,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution import ResolutionPlan


class ResolutionConflictDiagnosticAdapter:
    """Convert resolution-plan conflicts into resolution diagnostics."""

    def __init__(
        self,
        conflict_adapter: ResolutionConflictAdapter | None = None,
        diagnostic_adapter: ConflictDiagnosticAdapter | None = None,
    ) -> None:
        """Initialize the composite adapter."""

        self._conflict_adapter = (
            conflict_adapter
            if conflict_adapter is not None
            else ResolutionConflictAdapter()
        )
        self._diagnostic_adapter = (
            diagnostic_adapter
            if diagnostic_adapter is not None
            else ConflictDiagnosticAdapter()
        )

    def adapt(
        self,
        plan: ResolutionPlan,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return conflict diagnostics represented by a resolution plan."""

        conflicts = self._conflict_adapter.adapt(
            plan,
        )

        return self._diagnostic_adapter.adapt(
            conflicts,
        )
