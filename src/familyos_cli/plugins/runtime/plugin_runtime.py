"""Plugin runtime."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.capabilities.capability_provider import (
    CapabilityProvider,
)
from familyos_cli.plugins.capabilities.capability_registry import (
    CapabilityRegistry,
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
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_provider import (
    PluginContributionProvider,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_registry import PluginRegistry
from familyos_cli.plugins.runtime.plugin_collection import PluginCollection
from familyos_cli.plugins.runtime.runtime_context import RuntimeContext
from familyos_cli.plugins.runtime.runtime_state import RuntimeState


class PluginRuntime:
    """Manage active plugin instances and their capabilities and contributions."""

    def __init__(
        self,
        context: RuntimeContext | None = None,
    ) -> None:
        """Initialize runtime."""

        self._context = (
            context
            if context is not None
            else RuntimeContext()
        )

        self._registry = PluginRegistry()
        self._plugins = PluginCollection()

        self._capability_provider = CapabilityProvider()
        self._capability_registry = CapabilityRegistry()

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
        """Activate a plugin and register its capabilities and contributions."""

        plugin_name = self._plugin_name(
            plugin,
        )

        self._context.lifecycle.register(
            plugin_name,
        )

        self._context.lifecycle.transition(
            plugin_name,
            RuntimeState.INITIALIZED,
        )

        plugin.activate()

        self._context.lifecycle.transition(
            plugin_name,
            RuntimeState.ACTIVE,
        )

        self._plugins.add(
            plugin,
        )

        for capability in (
            self._capability_provider.capabilities(
                plugin,
            )
        ):
            self._capability_registry.register(
                capability,
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

        plugin_name = self._plugin_name(
            plugin,
        )

        self._context.lifecycle.transition(
            plugin_name,
            RuntimeState.STOPPING,
        )

        plugin.deactivate()

        self._context.lifecycle.transition(
            plugin_name,
            RuntimeState.STOPPED,
        )

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

    def generation_recipe_contributions(
        self,
    ) -> tuple[GenerationRecipeContribution, ...]:
        """Return generation recipe contributions."""

        return self._contribution_registry.get_all(
            GenerationRecipeContribution,
        )

    def domain_generation_contributions(
        self,
    ) -> tuple[DomainGenerationContribution, ...]:
        """Return domain generation contributions."""

        return self._contribution_registry.get_all(
            DomainGenerationContribution,
        )

    def template_contributions(
        self,
    ) -> tuple[TemplateContribution, ...]:
        """Return template contributions."""

        return self._contribution_registry.get_all(
            TemplateContribution,
        )

    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return plugin template directories."""

        return tuple(
            contribution.template_directory
            for contribution in self.template_contributions()
        )

    def capabilities(
        self,
    ) -> CapabilityRegistry:
        """Return capability registry."""

        return self._capability_registry

    def plugins(
        self,
    ) -> PluginCollection:
        """Return active plugin collection."""

        return self._plugins

    def registry(
        self,
    ) -> PluginRegistry:
        """Return plugin descriptor registry."""

        return self._registry

    def context(
        self,
    ) -> RuntimeContext:
        """Return the shared runtime context."""

        return self._context

    def state(
        self,
        plugin: Plugin,
    ) -> RuntimeState:
        """Return the runtime state of a plugin."""

        return self._context.lifecycle.state(
            self._plugin_name(
                plugin,
            ),
        )

    def _plugin_name(
        self,
        plugin: Plugin,
    ) -> str:
        """Return the plugin runtime identifier."""

        metadata = plugin.get_metadata()

        if metadata is not None:
            return metadata.name

        return type(plugin).__name__
