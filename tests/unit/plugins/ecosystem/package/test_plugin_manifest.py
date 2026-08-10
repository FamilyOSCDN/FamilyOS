"""Tests for the plugin manifest model."""

from familyos_cli.plugins.ecosystem.package import (
    PluginManifest,
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
)


def test_plugin_manifest_creation() -> None:
    package = PluginPackage(
        name="calendar",
        version="1.2.0",
        source="official",
    )
    dependency = PluginDependency(
        name="identity",
        minimum_version="1.0.0",
    )

    manifest = PluginManifest(
        package=package,
        dependencies=(
            dependency,
        ),
    )

    assert manifest.package == package
    assert manifest.dependencies == (
        dependency,
    )


def test_plugin_manifest_exposes_plugin_id() -> None:
    """Manifest should expose canonical package identity."""

    manifest = PluginManifest(
        package=PluginPackage(
            plugin_id="familyos.calendar",
            version="1.2.0",
            source="official",
        ),
    )

    assert manifest.plugin_id == "familyos.calendar"


def test_plugin_manifest_exposes_package_name() -> None:
    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.2.0",
            source="official",
        ),
    )

    assert manifest.name == "calendar"


def test_plugin_manifest_exposes_package_version() -> None:
    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.2.0",
            source="official",
        ),
    )

    assert manifest.version == "1.2.0"


def test_plugin_manifest_uses_package_identifier() -> None:
    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.2.0",
            source="official",
        ),
    )

    assert manifest.identifier() == "calendar@1.2.0"


def test_plugin_manifest_has_no_dependencies_by_default() -> None:
    manifest = PluginManifest(
        package=PluginPackage(
            name="calendar",
            version="1.2.0",
            source="official",
        ),
    )

    assert manifest.dependencies == ()
