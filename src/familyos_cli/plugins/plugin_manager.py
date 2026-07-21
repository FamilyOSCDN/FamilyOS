"""Plugin manager."""

from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_loader import PluginLoader


class PluginManager:
    """Manage installed FamilyOS plugins."""

    def __init__(
        self,
        plugins_directory: Path = Path("plugins"),
    ) -> None:
        """Initialize the plugin manager."""

        self._plugins_directory = plugins_directory
        self._loader = PluginLoader()

    def list(self) -> list[PluginDescriptor]:
        """Return installed plugins."""

        if not self._plugins_directory.exists():
            return []

        return sorted(
            (
                self._loader.load(plugin)
                for plugin in self._plugins_directory.iterdir()
                if plugin.is_dir()
            ),
            key=lambda plugin: plugin.id,
        )