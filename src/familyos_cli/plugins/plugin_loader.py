from __future__ import annotations

import importlib
from pathlib import Path

import yaml

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin


class PluginLoader:
    """Loads FamilyOS plugins dynamically."""

    def load(
        self,
        source: Path | PluginDescriptor,
    ) -> Plugin | PluginDescriptor:
        """Load plugin descriptor or plugin instance."""

        if isinstance(source, Path):
            return self._discover(source)

        module = importlib.import_module(source.module)

        plugin_class = getattr(
            module,
            source.class_name,
        )

        if not issubclass(plugin_class, Plugin):
            raise TypeError(
                f"{source.class_name} must inherit from Plugin"
            )

        return plugin_class()

    def _discover(
        self,
        plugin_path: Path,
    ) -> PluginDescriptor:
        """Discover plugin descriptor."""

        metadata_file = plugin_path / "plugin.yaml"

        data = yaml.safe_load(
            metadata_file.read_text(encoding="utf-8")
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
            enabled=data.get("enabled", True),
        )