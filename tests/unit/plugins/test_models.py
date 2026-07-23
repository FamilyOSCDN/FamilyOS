"""Tests for plugin models."""

from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor


def test_plugin_descriptor_should_store_data() -> None:
    """Plugin descriptor should expose its data."""

    plugin = PluginDescriptor(
        id="ddd",
        name="Domain Driven Design",
        version="1.0.0",
        author="FamilyOS Team",
        description="DDD plugin",
        module="familyos_cli.plugins.ddd.plugin",
        class_name="DDDPlugin",
        path=Path("plugins/ddd"),
        enabled=True,
    )

    assert plugin.id == "ddd"
    assert plugin.name == "Domain Driven Design"
    assert plugin.version == "1.0.0"
    assert plugin.author == "FamilyOS Team"
    assert plugin.description == "DDD plugin"
    assert plugin.module == "familyos_cli.plugins.ddd.plugin"
    assert plugin.class_name == "DDDPlugin"
    assert plugin.path == Path("plugins/ddd")
    assert plugin.enabled