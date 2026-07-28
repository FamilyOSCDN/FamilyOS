"""Registry for plugin contributions."""

from __future__ import annotations

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_contribution import PluginContribution


class PluginContributionRegistry:
    """Collect contributions from active plugins."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._contributions: list[PluginContribution] = []

    def register(
        self,
        plugin: Plugin,
    ) -> None:
        """Register a plugin contribution."""

        contribution = getattr(
            plugin,
            "contribution",
            None,
        )

        if callable(contribution):
            plugin_contribution = contribution()

            if plugin_contribution is not None:
                self._contributions.append(
                    plugin_contribution,
                )

    def all(
        self,
    ) -> tuple[PluginContribution, ...]:
        """Return all registered contributions."""
        return tuple(self._contributions)
