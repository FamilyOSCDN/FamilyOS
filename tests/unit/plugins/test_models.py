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
        path=Path("plugins/ddd"),
    )

    assert plugin.id == "ddd"
    assert plugin.name == "Domain Driven Design"
    assert plugin.version == "1.0.0"
    assert plugin.author == "FamilyOS Team"
    assert plugin.description == "DDD plugin"
    assert plugin.path == Path("plugins/ddd")