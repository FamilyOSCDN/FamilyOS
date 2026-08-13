"""Shared helper for loading a plugin instance during compliance validation."""

from __future__ import annotations

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader


def load_plugin_instance(
    descriptor: PluginDescriptor,
) -> Plugin:
    """Load and return the plugin instance described by a descriptor.

    Any error raised while importing or instantiating the plugin
    (ImportError, AttributeError, TypeError, etc.) propagates to the
    caller, which is expected to catch it and translate it into a FAIL or
    NOT_EVALUATED rule outcome rather than letting it crash validation.
    """

    result = PluginLoader().load(descriptor)

    if not isinstance(result, Plugin):
        raise TypeError(
            f"Expected a Plugin instance, got {type(result).__name__}",
        )

    return result
