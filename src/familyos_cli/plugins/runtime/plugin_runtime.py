from __future__ import annotations

from familyos_cli.plugins.hooks import HookRegistry
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_registry import PluginRegistry
from familyos_cli.plugins.runtime.hook_dispatcher import HookDispatcher
from familyos_cli.plugins.runtime.plugin_activator import PluginActivator


class PluginRuntime:
    """Runtime responsible for plugin registration and hook dispatching."""

    def __init__(self) -> None:
        """Initialize the plugin runtime."""
        self._plugin_registry = PluginRegistry()
        self._hook_registry = HookRegistry()

        self._dispatcher = HookDispatcher(
            self._hook_registry,
        )

        self._activator = PluginActivator(
            self._hook_registry,
        )

    def register(
        self,
        plugin: Plugin,
    ) -> None:
        """Register and activate a plugin."""
        self._plugin_registry.register(plugin)
        self._activator.activate(plugin)

    def plugins(self) -> PluginRegistry:
        """Return the plugin registry."""
        return self._plugin_registry

    def hooks(self) -> HookRegistry:
        """Return the hook registry."""
        return self._hook_registry

    def dispatch(
        self,
        event: str,
        context: object,
    ) -> None:
        """Dispatch a runtime event."""
        self._dispatcher.dispatch(
            event,
            context,
        )