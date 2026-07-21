from __future__ import annotations

from familyos_cli.plugins.plugin_context import PluginContext


class Plugin:
    """Base class for all FamilyOS plugins."""

    name: str = "plugin"
    version: str = "0.1.0"

    def before_generate(self, context: PluginContext) -> None:
        """Called before project generation."""
        return None

    def after_generate(self, context: PluginContext) -> None:
        """Called after project generation."""
        return None