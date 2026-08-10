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
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
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
from familyos_cli.plugins.runtime.plugin_collection import (
    PluginCollection,
)
from familyos_cli.plugins.runtime.runtime_context import (
    RuntimeContext,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


class PluginRuntime:
    """Manage active plugin instances and their runtime contributions."""

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

        self._plugins_by_id: dict[str, Plugin] = {}
        self._plugin_ids_by_instance: dict[int, str] = {}

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
        *,
        plugin_id: str | None = None,
    ) -> None:
        """Activate a plugin and register its runtime resources."""

        runtime_plugin_id = (
            plugin_id
            if plugin_id is not None
            else self._legacy_plugin_id(
                plugin,
            )
        )

        self._context.lifecycle.register(
            runtime_plugin_id,
        )

        self._context.lifecycle.transition(
            runtime_plugin_id,
            RuntimeState.INITIALIZED,
        )

        plugin.activate()

        self._context.lifecycle.transition(
            runtime_plugin_id,
            RuntimeState.ACTIVE,
        )

        self._plugins.add(
            plugin,
        )

        self._plugins_by_id[
            runtime_plugin_id
        ] = plugin

        self._plugin_ids_by_instance[
            id(plugin)
        ] = runtime_plugin_id

        for capability in (
            self._capability_provider.capabilities(
                plugin,
            )
        ):
            self._validate_capability_ownership(
                plugin_id=runtime_plugin_id,
                capability=capability,
            )

            self._capability_registry.register(
                capability,
            )

        for contribution in (
            self._contribution_provider.contributions(
                plugin,
            )
        ):
            self._validate_contribution_ownership(
                plugin_id=runtime_plugin_id,
                contribution=contribution,
            )

            self._contribution_registry.register(
                contribution,
            )

    def deactivate(
        self,
        plugin: Plugin,
    ) -> None:
        """Deactivate a plugin using its runtime identity."""

        runtime_plugin_id = self._runtime_plugin_id(
            plugin,
        )

        self._deactivate(
            plugin,
            runtime_plugin_id,
        )

    def deactivate_by_plugin_id(
        self,
        plugin_id: str,
    ) -> None:
        """Deactivate an active plugin by canonical identifier."""

        plugin = self.plugin(
            plugin_id,
        )

        self._deactivate(
            plugin,
            plugin_id,
        )

    def plugin(
        self,
        plugin_id: str,
    ) -> Plugin:
        """Return an active plugin by canonical identifier."""

        try:
            return self._plugins_by_id[
                plugin_id
            ]
        except KeyError as error:
            raise ValueError(
                f"Plugin '{plugin_id}' is not active.",
            ) from error

    def state_by_plugin_id(
        self,
        plugin_id: str,
    ) -> RuntimeState:
        """Return runtime state for a canonical plugin identifier."""

        return self._context.lifecycle.state(
            plugin_id,
        )

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch before-generate hooks."""

        for plugin in self._plugins.all():
            plugin.before_generate(
                context,
            )

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch after-generate hooks."""

        for plugin in self._plugins.all():
            plugin.after_generate(
                context,
            )

    def before_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch before-render hooks."""

        for plugin in self._plugins.all():
            plugin.before_render(
                context,
            )

    def after_render(
        self,
        context: GenerationContext,
    ) -> None:
        """Dispatch after-render hooks."""

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
        """Return domain-generation contributions."""

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
        """Return shared runtime context."""

        return self._context

    def state(
        self,
        plugin: Plugin,
    ) -> RuntimeState:
        """Return runtime state for a plugin."""

        return self._context.lifecycle.state(
            self._runtime_plugin_id(
                plugin,
            ),
        )

    def _deactivate(
        self,
        plugin: Plugin,
        plugin_id: str,
    ) -> None:
        """Deactivate an active plugin under its runtime identity."""

        self._context.lifecycle.transition(
            plugin_id,
            RuntimeState.STOPPING,
        )

        plugin.deactivate()

        self._context.lifecycle.transition(
            plugin_id,
            RuntimeState.STOPPED,
        )

        self._plugins.remove(
            plugin,
        )

        self._plugins_by_id.pop(
            plugin_id,
            None,
        )

        self._plugin_ids_by_instance.pop(
            id(plugin),
            None,
        )

    def _validate_capability_ownership(
        self,
        *,
        plugin_id: str,
        capability: PluginCapability,
    ) -> None:
        """Validate that a capability belongs to its providing plugin."""

        expected_prefix = f"{plugin_id}."

        if not capability.id.value.startswith(
            expected_prefix,
        ):
            raise ValueError(
                f"Capability '{capability.id}' "
                f"does not belong to plugin '{plugin_id}'.",
            )

    def _validate_contribution_ownership(
        self,
        *,
        plugin_id: str,
        contribution: Contribution,
    ) -> None:
        """Validate that a contribution belongs to its providing plugin."""

        expected_prefix = f"{plugin_id}."

        if not contribution.id.value.startswith(
            expected_prefix,
        ):
            raise ValueError(
                f"Contribution '{contribution.id}' "
                f"does not belong to plugin '{plugin_id}'.",
            )

    def _runtime_plugin_id(
        self,
        plugin: Plugin,
    ) -> str:
        """Return runtime identity associated with a plugin instance."""

        return self._plugin_ids_by_instance.get(
            id(plugin),
            self._legacy_plugin_id(
                plugin,
            ),
        )

    def _legacy_plugin_id(
        self,
        plugin: Plugin,
    ) -> str:
        """Return legacy identity for direct plugin activation."""

        metadata = plugin.get_metadata()

        if metadata is not None:
            return metadata.name

        return type(plugin).__name__
