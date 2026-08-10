"""Tests for plugin capabilities."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


def test_plugin_capability_creation() -> None:
    """Capabilities should preserve their public attributes."""

    capability = PluginCapability(
        id=PluginCapabilityId(
            "example.generation.domain",
        ),
        display_name="Domain Generation",
        description="Provides domain generation support.",
        metadata={
            "category": "generation",
        },
    )

    assert capability.id == PluginCapabilityId(
        "example.generation.domain",
    )
    assert capability.display_name == "Domain Generation"
    assert capability.description == (
        "Provides domain generation support."
    )
    assert capability.metadata == {
        "category": "generation",
    }


def test_plugin_capability_uses_empty_defaults() -> None:
    """Optional capability values should use safe defaults."""

    capability = PluginCapability(
        id=PluginCapabilityId(
            "example.generation.templates",
        ),
        display_name="Templates",
    )

    assert capability.description == ""
    assert capability.metadata == {}
