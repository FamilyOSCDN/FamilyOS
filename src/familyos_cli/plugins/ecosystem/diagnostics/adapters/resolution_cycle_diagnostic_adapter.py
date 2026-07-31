"""Adapter generating cycle diagnostics from resolution context."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.adapters.cycle_diagnostic_adapter import (
    CycleDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.diagnostics.detection import (
    CycleDetector,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.diagnostics.resolution_context import (
    ResolutionContext,
)


class ResolutionCycleDiagnosticAdapter:
    """Generate cycle diagnostics from a resolution context."""

    def __init__(
        self,
        cycle_adapter: CycleDiagnosticAdapter | None = None,
    ) -> None:
        """Initialize the adapter."""

        self._cycle_adapter = (
            cycle_adapter
            if cycle_adapter is not None
            else CycleDiagnosticAdapter()
        )

    def adapt(
        self,
        context: ResolutionContext,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return dependency cycle diagnostics."""

        if context.cycle_source is None:
            return ()

        cycles = CycleDetector(
            context.cycle_source,
        ).detect()

        return self._cycle_adapter.adapt(
            cycles,
        )
