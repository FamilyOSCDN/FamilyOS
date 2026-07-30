"""Tests for plugin package model."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def test_plugin_package_creation() -> None:
    """Plugin package should be created."""

    package = PluginPackage(
        name="calendar",
        version="1.0.0",
        source="official",
    )

    assert package.name == "calendar"
    assert package.version == "1.0.0"
    assert package.identifier() == "calendar@1.0.0"
