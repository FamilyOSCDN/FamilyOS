"""Tests for the plugin loader."""

from pathlib import Path

from familyos_cli.plugins.plugin_loader import PluginLoader


def test_load_should_return_plugin_descriptor(
    tmp_path: Path,
) -> None:
    """Loading a plugin should return a descriptor."""

    plugin_dir = tmp_path / "ddd"
    plugin_dir.mkdir()

    (plugin_dir / "plugin.yaml").write_text(
        """
id: ddd
name: Domain Driven Design
version: 1.0.0
author: FamilyOS Team
description: DDD plugin
""",
        encoding="utf-8",
    )

    loader = PluginLoader()

    plugin = loader.load(plugin_dir)

    assert plugin.id == "ddd"
    assert plugin.name == "Domain Driven Design"
    assert plugin.version == "1.0.0"
    assert plugin.author == "FamilyOS Team"
    assert plugin.description == "DDD plugin"
    assert plugin.path == plugin_dir