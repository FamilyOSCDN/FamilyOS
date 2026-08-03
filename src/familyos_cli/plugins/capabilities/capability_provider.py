"""Plugin capability provider."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.plugin import Plugin


class CapabilityProvider:
    """Extract capabilities from plugins."""

    def capabilities(
        self,
        plugin: Plugin,
    ) -> tuple[PluginCapability, ...]:
        """Return capabilities declared by a plugin."""

        return plugin.capabilities()
