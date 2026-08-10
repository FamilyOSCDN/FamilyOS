from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.identity import (
    normalize_plugin_id,
)
from familyos_cli.plugins.models import PluginDescriptor


@dataclass(slots=True)
class PluginRegistry:
    """Registry of available FamilyOS plugins."""

    _plugins: dict[str, PluginDescriptor] = field(default_factory=dict)

    def register(
        self,
        plugin: PluginDescriptor,
    ) -> None:
        """Register a plugin descriptor by canonical Plugin Identifier."""

        if plugin.id in self._plugins:
            raise ValueError(
                f"Plugin '{plugin.id}' is already registered",
            )

        self._plugins[plugin.id] = plugin

    def unregister(
        self,
        plugin_id: str,
    ) -> None:
        """Remove a plugin using canonical or known legacy identity."""

        canonical_plugin_id = normalize_plugin_id(
            plugin_id,
        )

        self._plugins.pop(
            canonical_plugin_id,
            None,
        )

    def get(
        self,
        plugin_id: str,
    ) -> PluginDescriptor | None:
        """Retrieve a plugin using canonical or known legacy identity."""

        canonical_plugin_id = normalize_plugin_id(
            plugin_id,
        )

        return self._plugins.get(
            canonical_plugin_id,
        )

    def list_plugins(
        self,
    ) -> list[PluginDescriptor]:
        """Return all registered plugins."""

        return list(
            self._plugins.values(),
        )
