from pathlib import Path

import pytest

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_registry import PluginRegistry


def create_descriptor() -> PluginDescriptor:
    """Create a test plugin descriptor."""

    return PluginDescriptor(
        id="familyos.dummy",
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

    assert registry.get("familyos.dummy") == plugin


def test_get_registered_plugin() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    result = registry.get("familyos.dummy")

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

    registry.unregister("familyos.dummy")

    assert registry.get("familyos.dummy") is None


def test_register_duplicate_plugin_raises() -> None:
    registry = PluginRegistry()

    plugin = create_descriptor()

    registry.register(plugin)

    with pytest.raises(ValueError):
        registry.register(plugin)


def test_registry_get_accepts_legacy_plugin_id_alias() -> None:
    """Registry lookup should accept a governed legacy Plugin Identifier."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS",
        description="Education plugin for tests",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
    )

    registry = PluginRegistry()
    registry.register(descriptor)

    assert registry.get("education") == descriptor
    assert registry.get("familyos.education") == descriptor


def test_registry_does_not_duplicate_legacy_identity() -> None:
    """Legacy lookup compatibility should not duplicate registry entries."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS",
        description="Education plugin for tests",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
    )

    registry = PluginRegistry()
    registry.register(descriptor)

    assert registry.list_plugins() == [descriptor]


def test_registry_unregister_accepts_legacy_plugin_id_alias() -> None:
    """Registry removal should accept a governed legacy identifier."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS",
        description="Education plugin for tests",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
    )

    registry = PluginRegistry()
    registry.register(descriptor)

    registry.unregister("education")

    assert registry.get("familyos.education") is None
    assert registry.list_plugins() == []
