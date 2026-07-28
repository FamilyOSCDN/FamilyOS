from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.plugin_manager import PluginManager


def test_load_all_should_activate_plugins(
    tmp_path: Path,
) -> None:
    """PluginManager should load and activate plugins."""

    plugin_dir = tmp_path / "sample"
    plugin_dir.mkdir()

    (plugin_dir / "plugin.yaml").write_text(
        """
id: sample
name: Sample Plugin
version: 1.0.0
author: FamilyOS Team
description: Sample plugin
module: familyos_cli.plugins.samples.sample_plugin
class: SamplePlugin
enabled: true
""",
        encoding="utf-8",
    )

    manager = PluginManager(
        tmp_path,
    )

    manager.load_all()

    runtime = manager.runtime()

    assert (
        len(
            runtime.plugins().all(),
        )
        == 1
    )
