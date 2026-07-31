"""Protocol for adapters consuming resolution contexts."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.diagnostics.resolution_context import (
    ResolutionContext,
)


class ResolutionContextDiagnosticAdapter(Protocol):
    """Adapt a resolution context into diagnostics."""

    def adapt(
        self,
        context: ResolutionContext,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return diagnostics from a resolution context."""
