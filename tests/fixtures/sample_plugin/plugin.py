from __future__ import annotations

from familyos_cli.plugins import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata


class SamplePlugin(Plugin):
    """Sample plugin used in tests."""

    metadata = PluginMetadata(
        name="Sample Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Plugin used for testing.",
    )
