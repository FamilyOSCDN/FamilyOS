"""Compliance rule applicability."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)


@dataclass(frozen=True, slots=True)
class RuleApplicability:
    """Describe which plugin classifications a rule applies to.

    An empty ``classifications`` tuple means the rule applies to every
    classification.
    """

    classifications: tuple[PluginClassification, ...] = ()

    def applies_to(
        self,
        classification: PluginClassification,
    ) -> bool:
        """Return whether the rule applies to the given classification."""

        if not self.classifications:
            return True

        return classification in self.classifications
