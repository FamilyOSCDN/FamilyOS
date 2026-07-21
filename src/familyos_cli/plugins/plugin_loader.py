"""Plugin loader."""

from pathlib import Path

import yaml

from familyos_cli.plugins.models import PluginDescriptor


class PluginLoader:
    """Load plugin descriptors."""

    def load(
        self,
        plugin_path: Path,
    ) -> PluginDescriptor:
        """Load one plugin."""

        manifest = plugin_path / "plugin.yaml"

        with manifest.open(encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return PluginDescriptor(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            author=data["author"],
            description=data["description"],
            path=plugin_path,
        )