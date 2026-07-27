from pathlib import Path

import pytest

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_registry import PluginRegistry


def create_descriptor() -> PluginDescriptor:
    """Create a test plugin descriptor."""

    return PluginDescriptor(
        id="dummy",
        name="Dummy Plugin",
        version="1.0.0",
        author="FamilyOS",
        description="Dummy plugin for tests",
        module="tests.fixtures.sample_plugin.plugin",
        class_name="DummyPlugin",
        path=Path("/tmp/dummy"),
    )


def test_register_plugin() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    assert registry.get("dummy") == plugin


def test_get_registered_plugin() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    result = registry.get("dummy")

    assert result == plugin


def test_list_registered_plugins() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    plugins = registry.list_plugins()

    assert plugins == [plugin]


def test_unregister_plugin() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    registry.unregister("dummy")

    assert registry.get("dummy") is None


def test_register_duplicate_plugin_raises() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    with pytest.raises(ValueError):
        registry.register(plugin)