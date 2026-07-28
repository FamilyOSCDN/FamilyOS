"""Tests for the plugin runtime."""

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class DummyPlugin(Plugin):
    """Dummy plugin."""

    metadata = PluginMetadata(
        name="dummy",
        version="1.0.0",
    )


def test_activate_plugin() -> None:
    """Activating a plugin should register it."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)

    assert runtime.plugins().plugins() == [plugin]
