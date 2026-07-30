"""Tests for PluginContributionProvider."""

from dataclasses import dataclass

from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_provider import (
    PluginContributionProvider,
)
from familyos_cli.plugins.plugin import Plugin


@dataclass(
    frozen=True,
    slots=True,
)
class DummyContribution(
    Contribution,
):
    """Contribution used by provider tests."""

    name: str


class V2Plugin(
    Plugin,
):
    """Plugin exposing contributions through the V2 API."""

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return V2 contributions."""

        return (
            DummyContribution(
                name="generation",
            ),
            DummyContribution(
                name="domain",
            ),
        )


class LegacyPlugin(
    Plugin,
):
    """Plugin exposing contributions through legacy methods."""

    def contribution(
        self,
    ) -> Contribution:
        """Return the primary legacy contribution."""

        return DummyContribution(
            name="generation",
        )

    def domain_contribution(
        self,
    ) -> Contribution:
        """Return the legacy domain contribution."""

        return DummyContribution(
            name="domain",
        )


class MixedPlugin(
    Plugin,
):
    """Plugin exposing both V2 and legacy contributions."""

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return the official V2 contribution."""

        return (
            DummyContribution(
                name="v2",
            ),
        )

    def contribution(
        self,
    ) -> Contribution:
        """Return a legacy contribution."""

        return DummyContribution(
            name="legacy",
        )


def test_collects_v2_plugin_contributions() -> None:
    provider = PluginContributionProvider()

    contributions = provider.contributions(
        V2Plugin(),
    )

    assert contributions == (
        DummyContribution(
            name="generation",
        ),
        DummyContribution(
            name="domain",
        ),
    )


def test_collects_legacy_plugin_contributions() -> None:
    provider = PluginContributionProvider()

    contributions = provider.contributions(
        LegacyPlugin(),
    )

    assert contributions == (
        DummyContribution(
            name="generation",
        ),
        DummyContribution(
            name="domain",
        ),
    )


def test_prefers_v2_api_over_legacy_methods() -> None:
    provider = PluginContributionProvider()

    contributions = provider.contributions(
        MixedPlugin(),
    )

    assert contributions == (
        DummyContribution(
            name="v2",
        ),
    )


def test_returns_empty_tuple_for_plugin_without_contributions() -> None:
    provider = PluginContributionProvider()

    contributions = provider.contributions(
        Plugin(),
    )

    assert contributions == ()
