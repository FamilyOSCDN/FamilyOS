"""Plugin factory."""

from __future__ import annotations

import importlib

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin


class PluginFactory:
    """Create plugin instances."""

    def create(
        self,
        descriptor: PluginDescriptor,
    ) -> Plugin:
        """Instantiate a plugin from its descriptor."""

        module = importlib.import_module(
            descriptor.module,
        )

        plugin_class = getattr(
            module,
            descriptor.class_name,
        )

        plugin = plugin_class()

        if not isinstance(
            plugin,
            Plugin,
        ):
            raise TypeError(
                f"{descriptor.class_name} is not a Plugin.",
            )

        return plugin
