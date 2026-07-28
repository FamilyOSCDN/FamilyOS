"""Plugin manager.

Coordinates plugin discovery, registration and activation.
"""

from __future__ import annotations

from builtins import list as builtin_list
from dataclasses import dataclass, field
from pathlib import Path

from familyos_cli.plugins.models.plugin_descriptor import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader
from familyos_cli.plugins.plugin_registry import PluginRegistry
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


@dataclass(slots=True)
class PluginManager:
    """Application service responsible for plugin lifecycle management."""

    plugins_directory: Path | None = None

    registry: PluginRegistry = field(
        default_factory=PluginRegistry,
    )

    _runtime: PluginRuntime = field(
        default_factory=PluginRuntime,
    )

    _plugins: dict[str, PluginDescriptor] = field(
        default_factory=dict,
    )

    def runtime(self) -> PluginRuntime:
        """Return plugin runtime."""

        return self._runtime

    def register(
        self,
        plugin: PluginDescriptor,
    ) -> None:
        """Register a plugin descriptor."""

        self._plugins[plugin.id] = plugin

        self.registry.register(plugin)

    def get(
        self,
        name: str,
    ) -> PluginDescriptor | None:
        """Retrieve a registered plugin."""

        return self._plugins.get(name)

    def list(
        self,
    ) -> builtin_list[PluginDescriptor]:
        """List available plugins."""

        if self.plugins_directory is None:
            return builtin_list(self._plugins.values())

        if not self.plugins_directory.exists():
            return []

        loader = PluginLoader()

        plugins: builtin_list[PluginDescriptor] = []

        for plugin_path in self.plugins_directory.iterdir():
            if not plugin_path.is_dir():
                continue

            descriptor = loader.load(plugin_path)

            if isinstance(
                descriptor,
                PluginDescriptor,
            ):
                plugins.append(descriptor)
                self.register(descriptor)

        return plugins

    def list_plugins(
        self,
    ) -> builtin_list[PluginDescriptor]:
        """Return all registered plugins."""

        return builtin_list(self._plugins.values())

    def load_all(
        self,
    ) -> None:
        """Load all plugins from directory."""

        for plugin in self.list():
            if plugin.enabled:
                self.activate(plugin.id)

    def activate(
        self,
        name: str,
    ) -> None:
        """Activate a plugin by name."""

        descriptor = self.get(name)

        if descriptor is None:
            raise ValueError(f"Unknown plugin: {name}")

        plugin = PluginLoader().load(descriptor)

        if isinstance(plugin, Plugin):
            self._runtime.activate(plugin)

    def deactivate(
        self,
        name: str,
    ) -> None:
        """Deactivate a plugin by name."""

        descriptor = self.get(name)

        if descriptor is None:
            raise ValueError(f"Unknown plugin: {name}")

        plugin = PluginLoader().load(descriptor)

        if isinstance(plugin, Plugin):
            self._runtime.deactivate(plugin)
