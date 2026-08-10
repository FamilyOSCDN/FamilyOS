"""Tests for plugin models."""

from pathlib import Path

from familyos_cli.plugins.models import PluginDescriptor


def test_plugin_descriptor_should_store_data() -> None:
    """Plugin descriptor should expose its data."""

    plugin = PluginDescriptor(
        id="familyos.ddd",
        name="Domain Driven Design",
        version="1.0.0",
        author="FamilyOS Team",
        description="DDD plugin",
        module="familyos_cli.plugins.ddd.plugin",
        class_name="DDDPlugin",
        path=Path("plugins/ddd"),
        enabled=True,
    )

    assert plugin.id == "familyos.ddd"
    assert plugin.name == "Domain Driven Design"
    assert plugin.version == "1.0.0"
    assert plugin.author == "FamilyOS Team"
    assert plugin.description == "DDD plugin"
    assert plugin.module == "familyos_cli.plugins.ddd.plugin"
    assert plugin.class_name == "DDDPlugin"
    assert plugin.path == Path("plugins/ddd")
    assert plugin.enabled


def test_plugin_descriptor_accepts_canonical_plugin_id() -> None:
    """Plugin descriptor should accept a canonical Plugin Identifier."""

    plugin = PluginDescriptor(
        id="acme.calendar",
        name="Calendar",
        version="1.0.0",
    )

    assert plugin.id == "acme.calendar"


def test_plugin_descriptor_rejects_legacy_plugin_id() -> None:
    """Plugin descriptor should reject a legacy short identifier."""

    import pytest

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginDescriptor(
            id="calendar",
            name="Calendar",
            version="1.0.0",
        )


def test_plugin_descriptor_rejects_invalid_plugin_id() -> None:
    """Plugin descriptor should reject an invalid Plugin Identifier."""

    import pytest

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginDescriptor(
            id="FamilyOS.Calendar",
            name="Calendar",
            version="1.0.0",
        )
