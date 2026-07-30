"""Tests for plugin lifecycle manager."""

from familyos_cli.plugins.ecosystem.lifecycle import (
    PluginLifecycleManager,
    PluginState,
)


def test_plugin_registration_starts_discovered() -> None:
    """Registered plugins should start discovered."""

    manager = PluginLifecycleManager()

    manager.register("calendar")

    assert manager.state("calendar") == PluginState.DISCOVERED


def test_plugin_transition_creates_event() -> None:
    """State transitions should create lifecycle events."""

    manager = PluginLifecycleManager()

    manager.register("calendar")

    event = manager.transition(
        "calendar",
        PluginState.INSTALLED,
    )

    assert event.previous_state == PluginState.DISCOVERED
    assert event.new_state == PluginState.INSTALLED
    assert manager.state("calendar") == PluginState.INSTALLED
