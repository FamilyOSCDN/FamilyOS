from pathlib import Path
from typing import cast

from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader


def communication_plugin_path() -> Path:
    """Return communication plugin directory."""

    return (
        Path(__file__).parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "communication"
    )


def find_communication_descriptor(
    descriptors: list[PluginDescriptor],
) -> PluginDescriptor:
    """Return communication plugin descriptor."""

    return next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "communication"
    )


def test_communication_plugin_descriptor_is_discovered() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        communication_plugin_path().parent,
    )

    communication = find_communication_descriptor(
        descriptors,
    )

    assert isinstance(
        communication,
        PluginDescriptor,
    )

    assert communication.name == (
        "FamilyOS Communication Plugin"
    )

    assert communication.module == (
        "familyos_cli.plugins.builtin.communication.plugin"
    )

    assert communication.class_name == (
        "CommunicationPlugin"
    )


def test_communication_plugin_can_be_loaded() -> None:
    loader = PluginLoader()

    descriptor = find_communication_descriptor(
        loader.discover(
            communication_plugin_path().parent,
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
        CommunicationPlugin,
    )


def test_loaded_communication_plugin_has_metadata() -> None:
    loader = PluginLoader()

    descriptor = find_communication_descriptor(
        loader.discover(
            communication_plugin_path().parent,
        ),
    )

    plugin = cast(
        CommunicationPlugin,
        loader.load(
            descriptor,
        ),
    )

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert metadata.name == (
        "FamilyOS Communication Plugin"
    )

    assert metadata.version == (
        "1.0.0"
    )
