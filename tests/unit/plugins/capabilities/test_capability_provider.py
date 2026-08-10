"""Tests for the capability provider."""

from familyos_cli.plugins.capabilities.capability_provider import (
    CapabilityProvider,
)
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)
from familyos_cli.plugins.plugin import Plugin


class SamplePlugin(Plugin):
    """Plugin exposing capabilities."""

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return plugin capabilities."""

        return (
            PluginCapability(
                id=PluginCapabilityId(
                    "example.generation.domain",
                ),
                display_name="Domain Generation",
            ),
            PluginCapability(
                id=PluginCapabilityId(
                    "example.generation.templates",
                ),
                display_name="Templates",
            ),
        )


class EmptyPlugin(Plugin):
    """Plugin without capabilities."""


def test_provider_returns_declared_capabilities() -> None:
    """Declared capabilities should be returned."""

    provider = CapabilityProvider()

    capabilities = provider.capabilities(
        SamplePlugin(),
    )

    assert len(capabilities) == 2
    assert capabilities[0].display_name == "Domain Generation"
    assert capabilities[1].display_name == "Templates"


def test_provider_returns_empty_tuple() -> None:
    """Plugins without capabilities should return an empty tuple."""

    provider = CapabilityProvider()

    assert provider.capabilities(
        EmptyPlugin(),
    ) == ()
