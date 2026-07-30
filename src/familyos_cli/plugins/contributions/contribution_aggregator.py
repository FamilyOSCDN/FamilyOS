"""Contribution aggregator."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.contributions.aggregated_contribution import (
    AggregatedContribution,
)
from familyos_cli.plugins.plugin_contribution import (
    PluginContribution,
)


class ContributionAggregator:
    """Aggregate plugin contributions."""

    def aggregate(
        self,
        contributions: tuple[PluginContribution, ...],
    ) -> AggregatedContribution:
        """Aggregate all plugin contributions."""

        if not contributions:
            return AggregatedContribution()

        templates: list[Path] = []

        specifications: list[Path] = []

        variables: dict[str, object] = {}

        generation_contributions = []

        for contribution in contributions:
            templates.extend(
                contribution.templates,
            )

            specifications.extend(
                contribution.specifications,
            )

            variables.update(
                contribution.variables,
            )

            generation_contributions.extend(
                contribution.generation_contributions,
            )

        return AggregatedContribution(
            templates=tuple(templates),
            specifications=tuple(specifications),
            variables=variables,
            generation_contributions=tuple(
                generation_contributions,
            ),
        )
