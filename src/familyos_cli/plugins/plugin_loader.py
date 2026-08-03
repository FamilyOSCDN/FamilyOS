"""Plugin loader.

Responsible for discovering and dynamically loading FamilyOS plugins.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import cast

import yaml

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_context import PluginContext


class PluginLoader:
    """Loads FamilyOS plugins dynamically."""

    def load(
        self,
        source: Path | PluginDescriptor,
        *,
        context: PluginContext | None = None,
    ) -> Plugin | PluginDescriptor:
        """Load plugin descriptor or plugin instance."""

        if isinstance(source, Path):
            return self._discover(source)

        module = importlib.import_module(source.module)

        plugin_class = cast(
            type[Plugin],
            getattr(
                module,
                source.class_name,
            ),
        )

        if not issubclass(plugin_class, Plugin):
            raise TypeError(
                f"{source.class_name} must inherit from Plugin",
            )

        return plugin_class(
            context,
        )

    def discover(
        self,
        directory: Path,
    ) -> list[PluginDescriptor]:
        """Discover all plugins in a directory."""

        plugins: list[PluginDescriptor] = []

        if not directory.exists():
            return plugins

        for plugin_path in directory.iterdir():
            if not plugin_path.is_dir():
                continue

            metadata_file = plugin_path / "plugin.yaml"

            if not metadata_file.exists():
                continue

            plugins.append(
                self._discover(
                    plugin_path,
                ),
            )

        return plugins

    def _discover(
        self,
        plugin_path: Path,
    ) -> PluginDescriptor:
        """Discover plugin descriptor."""

        metadata_file = plugin_path / "plugin.yaml"

        data = yaml.safe_load(
            metadata_file.read_text(
                encoding="utf-8",
            ),
        )

        return PluginDescriptor(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            author=data["author"],
            description=data["description"],
            module=data["module"],
            class_name=data["class"],
            path=plugin_path,
            enabled=data.get(
                "enabled",
                True,
            ),
        )
