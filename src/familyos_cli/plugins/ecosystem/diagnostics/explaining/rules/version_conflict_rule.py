"""Version conflict explanation rule."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_kind import (
    DiagnosticKind,
)
from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


class VersionConflictRule:
    """Explain version conflicts."""

    def supports(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> bool:
        """Return whether this rule supports the diagnostic."""

        return diagnostic.kind is DiagnosticKind.VERSION_CONFLICT

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        """Create a version conflict explanation."""

        return ResolutionExplanation(
            title="Plugin version conflict",
            summary=(
                "Plugin requirements cannot "
                "be satisfied together."
            ),
            causes=diagnostic.details,
            suggestions=(
                "Choose compatible plugin versions.",
            ),
        )
