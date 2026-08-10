from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_factory import PluginFactory


def test_create_plugin() -> None:
    """PluginFactory should instantiate a plugin."""

    descriptor = PluginDescriptor(
        id="familyos.sample",
        name="Sample Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Sample plugin",
        module="familyos_cli.plugins.samples.sample_plugin",
        class_name="SamplePlugin",
        path=Path("."),
        enabled=True,
    )

    factory = PluginFactory()

    plugin = factory.create(
        descriptor,
    )

    assert plugin is not None
    assert plugin.metadata.name == "Sample Plugin"
    assert plugin.metadata.version == "1.0.0"
