"""Tests for plugin lifecycle events."""

from familyos_cli.plugins.ecosystem.lifecycle import (
    LifecycleEvent,
    PluginState,
)


def test_lifecycle_event_creation() -> None:
    """Lifecycle events should store state transitions."""

    event = LifecycleEvent(
        plugin_id="familyos.calendar",
        previous_state=PluginState.INSTALLED,
        new_state=PluginState.ENABLED,
    )

    assert event.plugin_id == "familyos.calendar"
    assert event.previous_state == PluginState.INSTALLED
    assert event.new_state == PluginState.ENABLED


def test_lifecycle_event_rejects_non_canonical_plugin_id() -> None:
    """Lifecycle events should reject non-canonical plugin identifiers."""

    import pytest

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        LifecycleEvent(
            plugin_id="calendar",
            previous_state=PluginState.INSTALLED,
            new_state=PluginState.ENABLED,
        )
