"""Base plugin contract."""

from __future__ import annotations

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin_context import PluginContext


class Plugin:
    """Base class for FamilyOS plugins."""

    metadata: PluginMetadata | None = None

    def __init__(
        self,
        context: PluginContext | None = None,
    ) -> None:
        """Initialize plugin."""

        self.context = context

    def activate(
        self,
    ) -> None:
        """Activate plugin."""

        return None

    def deactivate(
        self,
    ) -> None:
        """Deactivate plugin."""

        return None

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return contributions exposed by the plugin."""

        return ()

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Called before generation."""

        _ = context

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Called after generation."""

        _ = context

    def before_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Called before rendering."""

        _ = context

    def after_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Called after rendering."""

        _ = context

    def get_metadata(
        self,
    ) -> PluginMetadata | None:
        """Return plugin metadata."""

        return self.metadata
