"""Protocol for resolution diagnostic adapters."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution import ResolutionPlan


class ResolutionDiagnosticAdapter(Protocol):
    """Adapt a resolution plan into plugin resolution diagnostics."""

    def adapt(
        self,
        plan: ResolutionPlan,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return diagnostics represented by the resolution plan."""
