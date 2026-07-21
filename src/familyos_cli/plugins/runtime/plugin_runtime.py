from __future__ import annotations

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_registry import PluginRegistry


class PluginRuntime:
    """Runtime responsible for managing loaded plugin instances."""

    def __init__(self) -> None:
        """Initialize the plugin runtime."""
        self._plugin_registry = PluginRegistry()

    def register(self, plugin: Plugin) -> None:
        """Register a plugin instance in the runtime."""
        self._plugin_registry.register(plugin)

    def plugins(self) -> PluginRegistry:
        """Return the runtime plugin registry."""
        return self._plugin_registry