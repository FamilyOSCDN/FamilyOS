from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_loader import PluginLoader


class PluginManager:
    """Discover and load plugins from a directory."""

    def __init__(
        self,
        plugins_directory: Path,
    ) -> None:
        """Initialize the plugin manager."""
        self._plugins_directory = plugins_directory
        self._loader = PluginLoader()

    def list(self) -> list[PluginDescriptor]:
        """Return all available plugins."""
        if not self._plugins_directory.exists():
            return []

        plugins: list[PluginDescriptor] = []

        for path in sorted(self._plugins_directory.iterdir()):
            if not path.is_dir():
                continue

            plugins.append(
                self._loader.load(path),
            )

        return plugins