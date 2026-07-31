"""Default explanation rule."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


class DefaultRule:
    """Fallback explanation rule."""

    def supports(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> bool:
        """Return whether this rule supports the diagnostic."""

        return True

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        """Create a fallback explanation."""

        return ResolutionExplanation(
            title="Plugin resolution issue",
            summary=(
                "An unknown plugin resolution "
                "issue occurred."
            ),
            causes=diagnostic.details,
            suggestions=(
                "Review plugin dependencies "
                "and configuration.",
            ),
        )
