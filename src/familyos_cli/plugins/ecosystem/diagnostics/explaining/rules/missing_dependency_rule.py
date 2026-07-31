"""Missing dependency explanation rule."""

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


class MissingDependencyRule:
    """Explain missing plugin dependencies."""

    def supports(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> bool:
        """Return whether this rule supports the diagnostic."""

        return diagnostic.kind is DiagnosticKind.MISSING_DEPENDENCY

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        """Create a missing dependency explanation."""

        return ResolutionExplanation(
            title="Missing plugin dependency",
            summary=(
                "A required plugin dependency "
                "is not available."
            ),
            causes=diagnostic.details,
            suggestions=(
                "Install the missing plugin "
                "or enable a repository.",
            ),
        )
