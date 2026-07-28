from __future__ import annotations

from familyos_cli.plugins.hooks import HookRegistry
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.runtime.lifecycle import Lifecycle


class PluginActivator:
    """Activate plugins by registering their lifecycle hooks."""

    def __init__(
        self,
        registry: HookRegistry,
    ) -> None:
        """Initialize the plugin activator."""
        self._registry = registry

    def activate(
        self,
        plugin: Plugin,
    ) -> None:
        """Register all lifecycle hooks exposed by a plugin."""
        self._register_hook(
            plugin,
            Lifecycle.INITIALIZE,
        )
        self._register_hook(
            plugin,
            Lifecycle.BEFORE_GENERATE,
        )
        self._register_hook(
            plugin,
            Lifecycle.AFTER_GENERATE,
        )
        self._register_hook(
            plugin,
            Lifecycle.SHUTDOWN,
        )

    def _register_hook(
        self,
        plugin: Plugin,
        event: str,
    ) -> None:
        """Register a lifecycle hook if implemented."""
        callback = getattr(
            plugin,
            event,
            None,
        )

        if callable(callback):
            self._registry.register(
                event,
                callback,
            )
