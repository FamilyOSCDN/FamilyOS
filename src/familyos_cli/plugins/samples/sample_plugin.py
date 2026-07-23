from __future__ import annotations

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_context import PluginContext
from familyos_cli.plugins.plugin_metadata import PluginMetadata


class SamplePlugin(Plugin):
    """Sample plugin used for unit testing."""

    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            name="Sample Plugin",
            version="1.0.0",
            author="FamilyOS Team",
            description="Sample plugin",
        )

    def before_generate(
        self,
        context: PluginContext,
    ) -> None:
        """Executed before project generation."""
        _ = context

    def after_generate(
        self,
        context: PluginContext,
    ) -> None:
        """Executed after project generation."""
        _ = context