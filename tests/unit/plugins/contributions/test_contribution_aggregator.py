from pathlib import Path

from familyos_cli.plugins.contributions.aggregated_contribution import (
    AggregatedContribution,
)
from familyos_cli.plugins.contributions.contribution_aggregator import (
    ContributionAggregator,
)
from familyos_cli.plugins.plugin_contribution import (
    PluginContribution,
)


def test_should_aggregate_single_contribution() -> None:
    """ContributionAggregator should aggregate one contribution."""

    contribution = PluginContribution(
        templates=(Path("templates"),),
        specifications=(Path("specifications"),),
        variables={
            "project": "FamilyOS",
        },
    )

    aggregator = ContributionAggregator()

    result = aggregator.aggregate(
        (contribution,),
    )

    assert result == AggregatedContribution(
        templates=(Path("templates"),),
        specifications=(Path("specifications"),),
        variables={
            "project": "FamilyOS",
        },
    )
