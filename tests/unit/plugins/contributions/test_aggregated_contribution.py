"""Tests for AggregatedContribution."""

from pathlib import Path

from familyos_cli.plugins.contributions.aggregated_contribution import (
    AggregatedContribution,
)


def test_should_create_empty_aggregated_contribution() -> None:
    """AggregatedContribution should be empty by default."""

    contribution = AggregatedContribution()

    assert contribution.templates == ()
    assert contribution.specifications == ()
    assert contribution.variables == {}


def test_should_create_aggregated_contribution() -> None:
    """AggregatedContribution should store its values."""

    contribution = AggregatedContribution(
        templates=(
            Path("templates"),
        ),
        specifications=(
            Path("specifications"),
        ),
        variables={
            "name": "FamilyOS",
        },
    )

    assert contribution.templates == (
        Path("templates"),
    )

    assert contribution.specifications == (
        Path("specifications"),
    )

    assert contribution.variables == {
        "name": "FamilyOS",
    }