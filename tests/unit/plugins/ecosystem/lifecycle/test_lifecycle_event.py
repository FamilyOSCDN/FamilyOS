"""Tests for lifecycle events."""

from familyos_cli.plugins.ecosystem.lifecycle import (
    LifecycleEvent,
    PluginState,
)


def test_lifecycle_event_creation() -> None:
    """Lifecycle events should store state transitions."""

    event = LifecycleEvent(
        plugin_name="calendar",
        previous_state=PluginState.INSTALLED,
        new_state=PluginState.ENABLED,
    )

    assert event.plugin_name == "calendar"
    assert event.previous_state == PluginState.INSTALLED
    assert event.new_state == PluginState.ENABLED
