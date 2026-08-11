"""Tests for plugin lifecycle manager."""

import pytest

from familyos_cli.plugins.ecosystem.lifecycle import (
    PluginLifecycleManager,
    PluginState,
)


def test_plugin_registration_starts_discovered() -> None:
    """Registered plugins should start discovered."""

    manager = PluginLifecycleManager()

    manager.register("familyos.calendar")

    assert manager.state("familyos.calendar") == PluginState.DISCOVERED


def test_plugin_transition_creates_event() -> None:
    """State transitions should create lifecycle events."""

    manager = PluginLifecycleManager()

    manager.register("familyos.calendar")

    event = manager.transition(
        "familyos.calendar",
        PluginState.INSTALLED,
    )

    assert event.previous_state == PluginState.DISCOVERED
    assert event.new_state == PluginState.INSTALLED
    assert manager.state("familyos.calendar") == PluginState.INSTALLED


def test_plugin_registration_rejects_non_canonical_plugin_id() -> None:
    """Lifecycle should reject non-canonical plugin identifiers."""

    manager = PluginLifecycleManager()

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        manager.register("calendar")


def test_plugin_transition_rejects_non_canonical_plugin_id() -> None:
    """Lifecycle transitions should reject non-canonical plugin identifiers."""

    manager = PluginLifecycleManager()

    manager.register("familyos.calendar")

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        manager.transition(
            "calendar",
            PluginState.INSTALLED,
        )
