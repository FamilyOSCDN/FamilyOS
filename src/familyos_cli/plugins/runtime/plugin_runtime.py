"""Plugin runtime."""

from __future__ import annotations

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.contributions.contribution_registry import (
    ContributionRegistry,
)
from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_provider import (
    PluginContributionProvider,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_registry import PluginRegistry
from familyos_cli.plugins.runtime.plugin_collection import PluginCollection


class PluginRuntime:
    """Manage active plugin instances and their contributions."""

    def __init__(
        self,
    ) -> None:
        """Initialize runtime."""

        self._registry = PluginRegistry()
        self._plugins = PluginCollection()

        self._contribution_provider = (
            PluginContributionProvider()
        )

        self._contribution_registry = (
            ContributionRegistry()
        )

    def activate(
        self,
        plugin: Plugin,
    ) -> None:
        """Activate a plugin and register its contributions."""

        plugin.activate()

        self._plugins.add(
            plugin,
        )

        for contribution in (
            self._contribution_provider.contributions(
                plugin,
            )
        ):
            self._contribution_registry.register(
                contribution,
            )

    def deactivate(
        self,
        plugin: Plugin,
    ) -> None:
        """Deactivate a plugin."""

        plugin.deactivate()

        self._plugins.remove(
            plugin,
        )

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch before_generate hook."""

        for plugin in self._plugins.all():
            plugin.before_generate(
                context,
            )

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch after_generate hook."""

        for plugin in self._plugins.all():
            plugin.after_generate(
                context,
            )

    def before_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch before_render hook."""

        for plugin in self._plugins.all():
            plugin.before_render(
                context,
            )

    def after_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch after_render hook."""

        for plugin in self._plugins.all():
            plugin.after_render(
                context,
            )

    def generation_contributions(
        self,
    ) -> tuple[GenerationContribution, ...]:
        """Return generation contributions."""

        return self._contribution_registry.get_all(
            GenerationContribution,
        )

    def domain_generation_contributions(
        self,
    ) -> tuple[
        DomainGenerationContribution,
        ...,
    ]:
        """Return domain generation contributions."""

        return self._contribution_registry.get_all(
            DomainGenerationContribution,
        )

    def plugins(
        self,
    ) -> PluginCollection:
        """Return active plugins."""

        return self._plugins

    def registry(
        self,
    ) -> PluginRegistry:
        """Return plugin descriptor registry."""

        return self._registry
