"""Dependency cycle explanation rule."""

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


class DependencyCycleRule:
    """Explain dependency cycles."""

    def supports(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> bool:
        """Return whether this rule supports the diagnostic."""

        return diagnostic.kind is DiagnosticKind.DEPENDENCY_CYCLE

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        """Create a dependency cycle explanation."""

        causes = (
            diagnostic.details
            if diagnostic.details
            else diagnostic.path
        )

        return ResolutionExplanation(
            title="Dependency cycle detected",
            summary=(
                "Plugins cannot be resolved because "
                "they depend on each other."
            ),
            causes=causes,
            suggestions=(
                "Remove one dependency "
                "from the cycle.",
            ),
        )
