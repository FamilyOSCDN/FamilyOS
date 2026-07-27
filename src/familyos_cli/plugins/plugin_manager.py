from __future__ import annotations

from builtins import list as builtin_list
from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class PluginManager:
    """Manage FamilyOS plugins."""

    def __init__(
        self,
        plugins_directory: Path,
    ) -> None:
        """Initialize plugin manager."""

        self.plugins_directory = plugins_directory
        self.loader = PluginLoader()
        self._runtime = PluginRuntime()

    def descriptors(self) -> builtin_list[PluginDescriptor]:
        """Return all available plugin descriptors."""

        if not self.plugins_directory.exists():
            return []

        descriptors: builtin_list[PluginDescriptor] = []

        for plugin_path in self.plugins_directory.iterdir():
            if not plugin_path.is_dir():
                continue

            descriptor = self.loader.load(plugin_path)

            assert isinstance(descriptor, PluginDescriptor)

            descriptors.append(descriptor)

        return descriptors

    def list(self) -> builtin_list[PluginDescriptor]:
        """Backward-compatible alias."""

        return self.descriptors()

    def list_plugins(self) -> builtin_list[PluginDescriptor]:
        """Backward-compatible alias."""

        return self.descriptors()

    def load_all(self) -> builtin_list[Plugin]:
        """Load and activate all plugins."""

        loaded_plugins: builtin_list[Plugin] = []

        for descriptor in self.descriptors():
            plugin = self.loader.load(descriptor)

            assert isinstance(plugin, Plugin)

            self._runtime.activate(plugin)
            loaded_plugins.append(plugin)

        return loaded_plugins

    def runtime(self) -> PluginRuntime:
        """Return plugin runtime."""

        return self._runtime