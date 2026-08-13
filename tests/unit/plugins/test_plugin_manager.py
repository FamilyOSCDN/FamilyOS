"""Tests for the plugin manager."""

from pathlib import Path
from unittest.mock import Mock, patch

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_manager import PluginManager


def test_list_should_return_empty_when_directory_does_not_exist() -> None:
    """Listing plugins should return an empty list."""

    manager = PluginManager(
        plugins_directory=Path("does_not_exist"),
    )

    assert manager.list() == []


@patch(
    "familyos_cli.plugins.plugin_manager.PluginLoader",
)
def test_list_should_use_plugin_loader(
    mock_loader_class: Mock,
    tmp_path: Path,
) -> None:
    """Plugin manager should delegate loading."""

    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    (plugins_dir / "ddd").mkdir()

    loader = Mock()
    mock_loader_class.return_value = loader

    descriptor = PluginDescriptor(
        id="familyos.ddd",
        name="Domain Driven Design",
        version="1.0.0",
        author="FamilyOS Team",
        description="DDD plugin",
        module="familyos_cli.plugins.ddd.plugin",
        class_name="DDDPlugin",
        path=plugins_dir / "ddd",
        enabled=True,
    )

    loader.load.return_value = descriptor

    manager = PluginManager(
        plugins_directory=plugins_dir,
    )

    plugins = manager.list()

    loader.load.assert_called_once_with(
        plugins_dir / "ddd",
    )

    assert plugins == [descriptor]


def test_manager_get_accepts_legacy_plugin_id_alias() -> None:
    """Manager lookup should accept a governed legacy Plugin Identifier."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Education plugin",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
        enabled=True,
    )

    manager = PluginManager()
    manager.register(descriptor)

    assert manager.get("education") == descriptor
    assert manager.get("familyos.education") == descriptor


def test_manager_stores_only_canonical_plugin_id() -> None:
    """Manager storage should contain only canonical Plugin Identifiers."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Education plugin",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
        enabled=True,
    )

    manager = PluginManager()
    manager.register(descriptor)

    assert manager.list_plugins() == [descriptor]
    assert "familyos.education" in manager._plugins
    assert "education" not in manager._plugins


@patch(
    "familyos_cli.plugins.plugin_manager.PluginLoader",
)
def test_manager_activate_accepts_legacy_plugin_id_alias(
    mock_loader_class: Mock,
) -> None:
    """Activation should resolve legacy identifiers canonically."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Education plugin",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
        enabled=True,
    )

    loader = Mock()
    mock_loader_class.return_value = loader
    loader.load.return_value = Mock()

    manager = PluginManager()
    manager.register(descriptor)

    manager.activate("education")

    loader.load.assert_called_once()


def test_manager_deactivate_accepts_legacy_plugin_id_alias() -> None:
    """Deactivation should resolve legacy identifiers canonically."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Education plugin",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
        enabled=True,
    )

    manager = PluginManager()
    manager.register(descriptor)

    runtime = Mock()
    manager._runtime = runtime

    manager.deactivate("education")

    runtime.deactivate_by_plugin_id.assert_called_once_with(
        "familyos.education",
    )


@patch(
    "familyos_cli.plugins.plugin_manager.PluginLoader",
)
def test_manager_deactivates_the_active_plugin_instance(
    mock_loader_class: Mock,
) -> None:
    """Manager should deactivate the instance previously activated."""

    descriptor = PluginDescriptor(
        id="familyos.education",
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Education plugin",
        module="familyos_cli.plugins.builtin.education.plugin",
        class_name="EducationPlugin",
        path=Path("/tmp/education"),
        enabled=True,
    )

    plugin = Plugin()

    loader = Mock()
    mock_loader_class.return_value = loader
    loader.load.return_value = plugin

    manager = PluginManager()
    manager.register(descriptor)

    manager.activate("education")

    assert (
        manager.runtime().plugin(
            "familyos.education",
        )
        is plugin
    )

    manager.deactivate("education")

    assert manager.runtime().plugins().all() == []

    assert loader.load.call_count == 1
