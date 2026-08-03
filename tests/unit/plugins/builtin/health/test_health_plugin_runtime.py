from pathlib import Path
from typing import cast

from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
)
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader


def health_plugin_path() -> Path:
    """Return health plugin directory."""

    return (
        Path(__file__).parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "health"
    )


def find_health_descriptor(
    descriptors: list[PluginDescriptor],
) -> PluginDescriptor:
    """Return health plugin descriptor."""

    return next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "familyos.health"
    )


def test_health_plugin_descriptor_is_discovered() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        health_plugin_path().parent,
    )

    health = find_health_descriptor(
        descriptors,
    )

    assert isinstance(
        health,
        PluginDescriptor,
    )

    assert health.name == (
        "FamilyOS Health Plugin"
    )

    assert health.module == (
        "familyos_cli.plugins.builtin.health.plugin"
    )

    assert health.class_name == (
        "HealthPlugin"
    )


def test_health_plugin_can_be_loaded() -> None:
    loader = PluginLoader()

    descriptor = find_health_descriptor(
        loader.discover(
            health_plugin_path().parent,
        ),
    )

    plugin = cast(
        Plugin,
        loader.load(
            descriptor,
        ),
    )

    assert isinstance(
        plugin,
        HealthPlugin,
    )


def test_loaded_health_plugin_has_metadata() -> None:
    loader = PluginLoader()

    descriptor = find_health_descriptor(
        loader.discover(
            health_plugin_path().parent,
        ),
    )

    plugin = cast(
        Plugin,
        loader.load(
            descriptor,
        ),
    )

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert metadata.name == (
        "FamilyOS Health Plugin"
    )

    assert metadata.version == (
        "1.0.0"
    )
