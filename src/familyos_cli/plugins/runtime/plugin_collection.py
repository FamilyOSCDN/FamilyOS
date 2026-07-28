from __future__ import annotations

from familyos_cli.plugins.plugin import Plugin


class PluginCollection:
    """Collection of active plugins."""

    def __init__(self) -> None:
        """Initialize collection."""

        self._plugins: list[Plugin] = []

    def add(
        self,
        plugin: Plugin,
    ) -> None:
        """Add a plugin."""

        self._plugins.append(plugin)

    def remove(
        self,
        plugin: Plugin,
    ) -> None:
        """Remove a plugin."""

        if plugin in self._plugins:
            self._plugins.remove(plugin)

    def all(self) -> list[Plugin]:
        """Return all active plugins."""

        return self._plugins

    def plugins(self) -> list[Plugin]:
        """Backward-compatible alias for all()."""

        return self.all()
