"""Plugin runtime factory."""

from __future__ import annotations

from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


class RuntimeFactory:
    """Create plugin runtime instances."""

    @staticmethod
    def create() -> PluginRuntime:
        """Create a configured plugin runtime."""

        return PluginRuntime()
