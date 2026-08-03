from pathlib import Path
from typing import cast

from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
)
from familyos_cli.plugins.builtin.security.validation.security_validator import (
    SecurityValidator,
)
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader


def security_plugin_path() -> Path:
    """Return security plugin directory."""

    return (
        Path(__file__).parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "security"
    )


def find_security_descriptor(
    descriptors: list[PluginDescriptor],
) -> PluginDescriptor:
    """Return security plugin descriptor."""

    return next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "familyos.security"
    )


def test_security_plugin_descriptor_is_discovered() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        security_plugin_path().parent,
    )

    security = find_security_descriptor(
        descriptors,
    )

    assert isinstance(
        security,
        PluginDescriptor,
    )

    assert security.name == (
        "FamilyOS Security Plugin"
    )

    assert security.module == (
        "familyos_cli.plugins.builtin.security.plugin"
    )

    assert security.class_name == (
        "SecurityPlugin"
    )


def test_security_plugin_can_be_loaded() -> None:
    loader = PluginLoader()

    descriptor = find_security_descriptor(
        loader.discover(
            security_plugin_path().parent,
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
        SecurityPlugin,
    )


def test_loaded_security_plugin_has_metadata() -> None:
    loader = PluginLoader()

    descriptor = find_security_descriptor(
        loader.discover(
            security_plugin_path().parent,
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
        "FamilyOS Security Plugin"
    )

    assert metadata.version == (
        "1.0.0"
    )


def test_loaded_security_plugin_exposes_validator() -> None:
    loader = PluginLoader()

    descriptor = find_security_descriptor(
        loader.discover(
            security_plugin_path().parent,
        ),
    )

    plugin = cast(
        SecurityPlugin,
        loader.load(
            descriptor,
        ),
    )

    validator = plugin.validator()

    assert isinstance(
        validator,
        SecurityValidator,
    )
