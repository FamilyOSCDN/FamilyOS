from __future__ import annotations

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin import Plugin


class SamplePlugin(Plugin):
    """Sample plugin used for unit testing."""

    metadata = PluginMetadata(
        name="Sample Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Sample plugin",
    )

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Executed before project generation."""

        _ = context

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Executed after project generation."""

        _ = context