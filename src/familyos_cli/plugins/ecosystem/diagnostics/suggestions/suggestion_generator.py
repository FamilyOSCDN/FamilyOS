"""Generate resolution suggestions from diagnostics."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_kind import (
    DiagnosticKind,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.diagnostics.suggestions.resolution_suggestion import (
    ResolutionSuggestion,
)


class SuggestionGenerator:
    """Generate suggestions for plugin resolution diagnostics."""

    def generate(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> tuple[ResolutionSuggestion, ...]:
        """Generate suggestions for a diagnostic."""

        if diagnostic.kind is DiagnosticKind.MISSING_DEPENDENCY:
            return (
                ResolutionSuggestion(
                    message=(
                        "Install the missing plugin or "
                        "enable an appropriate repository."
                    ),
                ),
            )

        if diagnostic.kind is DiagnosticKind.DEPENDENCY_CYCLE:
            return (
                ResolutionSuggestion(
                    message=(
                        "Review the dependency graph "
                        "to remove the cycle."
                    ),
                ),
            )

        if diagnostic.kind is DiagnosticKind.VERSION_CONFLICT:
            return (
                ResolutionSuggestion(
                    message=(
                        "Review the requested plugin "
                        "versions for compatibility."
                    ),
                ),
            )

        return ()
