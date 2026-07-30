"""Tests for plugin lifecycle states."""

from familyos_cli.plugins.ecosystem.lifecycle import (
    PluginState,
)


def test_plugin_state_values() -> None:
    """Plugin states should expose expected values."""

    assert PluginState.DISCOVERED.value == "discovered"
    assert PluginState.INSTALLED.value == "installed"
    assert PluginState.ENABLED.value == "enabled"
    assert PluginState.REMOVED.value == "removed"
