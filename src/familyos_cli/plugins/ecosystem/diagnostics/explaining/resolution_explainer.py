"""Resolution diagnostic explanation service."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.explaining.rules import (
    DefaultRule,
    DependencyCycleRule,
    ExplanationRuleRegistry,
    MissingDependencyRule,
    VersionConflictRule,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


class ResolutionExplainer:
    """Explain plugin resolution diagnostics."""

    def __init__(
        self,
        registry: ExplanationRuleRegistry | None = None,
    ) -> None:
        """Initialize the explainer."""

        self._registry = (
            registry
            if registry is not None
            else ExplanationRuleRegistry(
                (
                    MissingDependencyRule(),
                    VersionConflictRule(),
                    DependencyCycleRule(),
                    DefaultRule(),
                ),
            )
        )

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        """Create a human-oriented explanation."""

        rule = self._registry.find(
            diagnostic,
        )

        return rule.explain(
            diagnostic,
        )
