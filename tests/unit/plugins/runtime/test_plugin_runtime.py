"""Tests for the plugin runtime."""

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime
from familyos_cli.plugins.runtime.runtime_context import RuntimeContext
from familyos_cli.plugins.runtime.runtime_state import RuntimeState


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


def test_activate_plugin_sets_active_state() -> None:
    """Activating a plugin should set its runtime state."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)

    assert runtime.state(plugin) == RuntimeState.ACTIVE


def test_deactivate_plugin_sets_stopped_state() -> None:
    """Deactivating a plugin should stop its runtime."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)
    runtime.deactivate(plugin)

    assert runtime.state(plugin) == RuntimeState.STOPPED
    assert runtime.plugins().plugins() == []


def test_runtime_accepts_context() -> None:
    """Runtime should accept an injected context."""

    context = RuntimeContext()

    runtime = PluginRuntime(
        context=context,
    )

    assert runtime.context() is context
