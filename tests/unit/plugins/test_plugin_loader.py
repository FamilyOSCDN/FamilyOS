"""Tests for the plugin loader."""

from pathlib import Path

import pytest

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_loader import PluginLoader


def test_load_should_return_plugin_descriptor(
    tmp_path: Path,
) -> None:
    """Loading a plugin should return a descriptor."""

    plugin_dir = tmp_path / "ddd"
    plugin_dir.mkdir()

    (plugin_dir / "plugin.yaml").write_text(
        """
id: familyos.ddd
name: Domain Driven Design
version: 1.0.0
author: FamilyOS Team
description: DDD plugin
module: familyos_cli.plugins.ddd.plugin
class: DDDPlugin
enabled: true
""",
        encoding="utf-8",
    )

    loader = PluginLoader()

    plugin = loader.load(
        plugin_dir,
    )

    assert isinstance(
        plugin,
        PluginDescriptor,
    )

    assert plugin.id == "familyos.ddd"
    assert plugin.name == "Domain Driven Design"
    assert plugin.version == "1.0.0"
    assert plugin.author == "FamilyOS Team"
    assert plugin.description == "DDD plugin"
    assert plugin.module == "familyos_cli.plugins.ddd.plugin"
    assert plugin.class_name == "DDDPlugin"
    assert plugin.path == plugin_dir
    assert plugin.enabled is True


def test_load_should_reject_non_canonical_plugin_id(
    tmp_path: Path,
) -> None:
    """Loading should reject a non-canonical Plugin Identifier."""

    plugin_dir = tmp_path / "ddd"
    plugin_dir.mkdir()

    (plugin_dir / "plugin.yaml").write_text(
        """
id: ddd
name: Domain Driven Design
version: 1.0.0
author: FamilyOS Team
description: DDD plugin
module: familyos_cli.plugins.ddd.plugin
class: DDDPlugin
enabled: true
""",
        encoding="utf-8",
    )

    loader = PluginLoader()

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        loader.load(
            plugin_dir,
        )
