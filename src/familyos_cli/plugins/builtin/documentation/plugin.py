from __future__ import annotations

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin import Plugin


class DocumentationPlugin(Plugin):
    """Built-in documentation plugin."""

    metadata = PluginMetadata(
        name="Documentation Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Generates project documentation.",
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
