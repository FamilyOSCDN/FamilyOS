"""Explanation rule protocol."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


class ExplanationRule(Protocol):
    """Define a rule able to explain a diagnostic."""

    def supports(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> bool:
        """Return whether this rule handles the diagnostic."""

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        """Create an explanation for the diagnostic."""
