from __future__ import annotations

from familyos_cli.plugins.plugin import Plugin


class PluginRegistry:
    """Registry of available plugins."""

    def __init__(self) -> None:
        """Initialize an empty plugin registry."""
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        """Register a plugin.

        Raises:
            ValueError: If a plugin with the same name is already registered.
        """
        name = plugin.metadata.name

        if name in self._plugins:
            raise ValueError(f"Plugin '{name}' is already registered.")

        self._plugins[name] = plugin

    def unregister(self, name: str) -> None:
        """Unregister a plugin."""
        self._plugins.pop(name, None)

    def exists(self, name: str) -> bool:
        """Return True if a plugin with the given name is registered."""
        return name in self._plugins

    def get(self, name: str) -> Plugin | None:
        """Return a registered plugin by name, or None if it does not exist."""
        return self._plugins.get(name)

    def list(self) -> list[Plugin]:
        """Return all registered plugins."""
        return list(self._plugins.values())