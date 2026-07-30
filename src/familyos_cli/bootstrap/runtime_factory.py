"""Plugin runtime factory."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.plugin_manager import (
    PluginManager,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


class RuntimeFactory:
    """Create plugin runtime instances."""

    @staticmethod
    def create() -> PluginRuntime:
        """Create a configured plugin runtime."""

        builtin_plugins_directory = (
            Path(__file__).resolve().parents[1]
            / "plugins"
            / "builtin"
        )

        manager = PluginManager(
            plugins_directory=builtin_plugins_directory,
        )

        manager.load_all()

        return manager.runtime()
