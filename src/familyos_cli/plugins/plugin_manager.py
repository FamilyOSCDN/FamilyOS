from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_factory import PluginFactory
from familyos_cli.plugins.plugin_loader import PluginLoader
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class PluginManager:
    """Discover, instantiate and activate plugins."""

    def __init__(
        self,
        plugins_directory: Path,
    ) -> None:
        """Initialize the plugin manager."""
        self._plugins_directory = plugins_directory
        self._loader = PluginLoader()
        self._factory = PluginFactory()
        self._runtime = PluginRuntime()

    def list(self) -> list[PluginDescriptor]:
        """Return all available plugin descriptors."""
        if not self._plugins_directory.exists():
            return []

        descriptors: list[PluginDescriptor] = []

        for path in sorted(self._plugins_directory.iterdir()):
            if not path.is_dir():
                continue

            descriptors.append(
                self._loader.load(path),
            )

        return descriptors

    def load_all(self) -> None:
        """Load and activate every enabled plugin."""
        for descriptor in self.list():
            if not descriptor.enabled:
                continue

            plugin = self._factory.create(
                descriptor,
            )

            self._runtime.register(
                plugin,
            )

    def runtime(self) -> PluginRuntime:
        """Return the runtime."""
        return self._runtime