import pytest

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.plugin_registry import PluginRegistry


class DummyPlugin(Plugin):
    metadata = PluginMetadata(
        name="dummy",
        version="1.0.0",
    )


def test_register_plugin() -> None:
    registry = PluginRegistry()

    plugin = DummyPlugin()

    registry.register(plugin)

    assert registry.exists("dummy")


def test_get_registered_plugin() -> None:
    registry = PluginRegistry()

    plugin = DummyPlugin()

    registry.register(plugin)

    assert registry.get("dummy") is plugin


def test_list_registered_plugins() -> None:
    registry = PluginRegistry()

    plugin = DummyPlugin()

    registry.register(plugin)

    assert registry.list() == [plugin]


def test_unregister_plugin() -> None:
    registry = PluginRegistry()

    plugin = DummyPlugin()

    registry.register(plugin)

    registry.unregister("dummy")

    assert not registry.exists("dummy")


def test_register_duplicate_plugin_raises() -> None:
    registry = PluginRegistry()

    registry.register(DummyPlugin())

    with pytest.raises(ValueError):
        registry.register(DummyPlugin())