"""Tests for the capability registry."""

import pytest

from familyos_cli.plugins.capabilities.capability_registry import (
    CapabilityRegistry,
)
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


def capability() -> PluginCapability:
    """Create a reusable capability."""

    return PluginCapability(
        id=PluginCapabilityId(
            "example.generation.domain",
        ),
        display_name="Domain Generation",
    )


def test_register_and_get_capability() -> None:
    """Registered capabilities should be retrievable."""

    registry = CapabilityRegistry()

    item = capability()

    registry.register(
        item,
    )

    assert registry.get(
        item.id,
    ) == item


def test_contains_capability() -> None:
    """Registry should report contained capabilities."""

    registry = CapabilityRegistry()

    item = capability()

    registry.register(
        item,
    )

    assert registry.contains(
        item.id,
    )


def test_duplicate_registration_raises() -> None:
    """Duplicate registrations should fail."""

    registry = CapabilityRegistry()

    item = capability()

    registry.register(
        item,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            item,
        )


def test_clear_registry() -> None:
    """Clearing the registry should remove all capabilities."""

    registry = CapabilityRegistry()

    registry.register(
        capability(),
    )

    registry.clear()

    assert registry.list() == ()
