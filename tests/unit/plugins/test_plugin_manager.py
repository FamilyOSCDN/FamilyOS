"""Tests for the plugin manager."""

from pathlib import Path
from unittest.mock import Mock, patch

from familyos_cli.plugins.models import PluginDescriptor
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
    mock_loader_class,
    tmp_path: Path,
) -> None:
    """Plugin manager should delegate loading."""

    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    (plugins_dir / "ddd").mkdir()

    loader = Mock()
    mock_loader_class.return_value = loader

    descriptor = PluginDescriptor(
        id="ddd",
        name="Domain Driven Design",
        version="1.0.0",
        author="FamilyOS Team",
        description="DDD plugin",
        path=plugins_dir / "ddd",
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