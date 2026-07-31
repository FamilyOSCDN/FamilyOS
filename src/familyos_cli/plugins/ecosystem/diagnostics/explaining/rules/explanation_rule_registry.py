"""Explanation rule registry."""

from __future__ import annotations

from collections.abc import Iterable

from familyos_cli.plugins.ecosystem.diagnostics.explaining.rules.explanation_rule import (
    ExplanationRule,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


class ExplanationRuleRegistry:
    """Registry of diagnostic explanation rules."""

    def __init__(
        self,
        rules: Iterable[ExplanationRule],
    ) -> None:
        """Initialize the registry."""

        self._rules = tuple(
            rules,
        )

    def find(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ExplanationRule:
        """Return the first rule supporting the diagnostic."""

        for rule in self._rules:
            if rule.supports(
                diagnostic,
            ):
                return rule

        raise LookupError(
            "No explanation rule supports the diagnostic.",
        )

    def rules(
        self,
    ) -> tuple[ExplanationRule, ...]:
        """Return registered rules."""

        return self._rules
