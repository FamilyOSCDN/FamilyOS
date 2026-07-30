"""Tests for the generic contribution registry."""

from dataclasses import dataclass

import pytest

from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.contributions.contribution_registry import (
    ContributionRegistry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class FirstContribution(
    Contribution,
):
    """Test contribution."""

    name: str


@dataclass(
    frozen=True,
    slots=True,
)
class SecondContribution(
    Contribution,
):
    """Second test contribution."""

    value: int


def test_registers_and_returns_contributions_by_type() -> None:
    registry = ContributionRegistry()

    first = FirstContribution(
        name="first",
    )
    second = FirstContribution(
        name="second",
    )

    registry.register(first)
    registry.register(second)

    assert registry.get_all(FirstContribution) == (
        first,
        second,
    )


def test_keeps_contribution_types_separated() -> None:
    registry = ContributionRegistry()

    first = FirstContribution(
        name="first",
    )
    second = SecondContribution(
        value=2,
    )

    registry.register(first)
    registry.register(second)

    assert registry.get_all(FirstContribution) == (
        first,
    )
    assert registry.get_all(SecondContribution) == (
        second,
    )


def test_returns_all_registered_contributions() -> None:
    registry = ContributionRegistry()

    first = FirstContribution(
        name="first",
    )
    second = SecondContribution(
        value=2,
    )

    registry.register(first)
    registry.register(second)

    assert registry.all() == (
        first,
        second,
    )


def test_rejects_duplicate_contribution() -> None:
    registry = ContributionRegistry()

    contribution = FirstContribution(
        name="duplicate",
    )

    registry.register(contribution)

    with pytest.raises(
        ValueError,
        match="Contribution already registered",
    ):
        registry.register(contribution)


def test_unregisters_contribution() -> None:
    registry = ContributionRegistry()

    contribution = FirstContribution(
        name="removable",
    )

    registry.register(contribution)
    registry.unregister(contribution)

    assert registry.get_all(FirstContribution) == ()
    assert registry.all() == ()


def test_reports_registered_types() -> None:
    registry = ContributionRegistry()

    registry.register(
        FirstContribution(
            name="first",
        ),
    )
    registry.register(
        SecondContribution(
            value=2,
        ),
    )

    assert registry.types() == (
        FirstContribution,
        SecondContribution,
    )


def test_supports_iteration_and_length() -> None:
    registry = ContributionRegistry()

    first = FirstContribution(
        name="first",
    )
    second = SecondContribution(
        value=2,
    )

    registry.register(first)
    registry.register(second)

    assert tuple(registry) == (
        first,
        second,
    )
    assert len(registry) == 2
