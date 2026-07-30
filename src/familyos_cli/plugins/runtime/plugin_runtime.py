from __future__ import annotations

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.contributions.aggregated_contribution import (
    AggregatedContribution,
)
from familyos_cli.plugins.contributions.contribution_aggregator import (
    ContributionAggregator,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.generation_contribution_registry import (
    GenerationContributionRegistry,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_registry import PluginRegistry
from familyos_cli.plugins.runtime.plugin_collection import PluginCollection
from familyos_cli.plugins.runtime.plugin_contribution_registry import (
    PluginContributionRegistry,
)


class PluginRuntime:
    """Manage active plugin instances."""

    def __init__(self) -> None:
        """Initialize runtime."""

        self._registry = PluginRegistry()
        self._plugins = PluginCollection()

        self._contributions = PluginContributionRegistry()

        self._generation_contributions = (
            GenerationContributionRegistry()
        )

    def activate(
        self,
        plugin: Plugin,
    ) -> None:
        """Activate a plugin."""

        plugin.activate()

        self._plugins.add(plugin)

        self._contributions.register(
            plugin,
        )

        contribution = getattr(
            plugin,
            "contribution",
            None,
        )

        if callable(contribution):
            plugin_contribution = contribution()

            if isinstance(
                plugin_contribution,
                GenerationContribution,
            ):
                self._generation_contributions.register(
                    plugin_contribution,
                )

    def deactivate(
        self,
        plugin: Plugin,
    ) -> None:
        """Deactivate a plugin."""

        plugin.deactivate()
        self._plugins.remove(plugin)

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch before_generate hook."""

        for plugin in self._plugins.all():
            plugin.before_generate(context)

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch after_generate hook."""

        for plugin in self._plugins.all():
            plugin.after_generate(context)

    def before_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch before_render hook."""

        for plugin in self._plugins.all():
            plugin.before_render(context)

    def after_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch after_render hook."""

        for plugin in self._plugins.all():
            plugin.after_render(context)

    def contributions(
        self,
    ) -> AggregatedContribution:
        """Return aggregated plugin contributions."""

        return ContributionAggregator().aggregate(
            self._contributions.all(),
        )

    def generation_contributions(
        self,
    ) -> tuple[GenerationContribution, ...]:
        """Return generation contributions."""

        return self._generation_contributions.all()

    def plugins(
        self,
    ) -> PluginCollection:
        """Return active plugins."""

        return self._plugins

    def registry(
        self,
    ) -> PluginRegistry:
        """Return plugin registry."""
        
        return self._registry
