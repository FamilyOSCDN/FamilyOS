"""Tests for plugin discovery service."""

from pathlib import Path

from familyos_cli.application.ports.plugins import (
    PluginDiscoveryPort,
)
from familyos_cli.plugins.ecosystem.discovery import (
    PluginDiscovery,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)


def write_plugin_manifest(
    plugin_directory: Path,
    *,
    plugin_id: str,
    name: str,
    version: str,
    enabled: bool = True,
) -> None:
    """Write a plugin manifest for discovery tests."""

    plugin_directory.mkdir(
        parents=True,
    )

    (plugin_directory / "plugin.yaml").write_text(
        (
            f"id: {plugin_id}\n"
            f"name: {name}\n"
            f"version: {version}\n"
            "author: FamilyOS Team\n"
            "description: Test plugin.\n"
            f"module: tests.fixtures.{plugin_id}.plugin\n"
            "class: TestPlugin\n"
            f"enabled: {str(enabled).lower()}\n"
        ),
        encoding="utf-8",
    )


def test_plugin_discovery_implements_discovery_port() -> None:
    """Discovery service should implement the application port."""

    discovery = PluginDiscovery()

    assert isinstance(discovery, PluginDiscoveryPort)


def test_discovery_returns_packages_from_local_repository(
    tmp_path: Path,
) -> None:
    """Discovery should map local descriptors to packages."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="calendar",
        name="Calendar Plugin",
        version="1.2.0",
    )

    repository = PluginRepository(
        name="Local Plugins",
        url=str(tmp_path),
        repository_type="local",
    )

    discovery = PluginDiscovery()

    packages = discovery.discover(repository)

    assert len(packages) == 1
    assert packages[0].name == "Calendar Plugin"
    assert packages[0].version == "1.2.0"
    assert packages[0].source == "Local Plugins"
    assert packages[0].identifier() == "Calendar Plugin@1.2.0"


def test_discovery_returns_multiple_local_packages(
    tmp_path: Path,
) -> None:
    """Discovery should return every active local plugin package."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="calendar",
        name="Calendar Plugin",
        version="1.0.0",
    )
    write_plugin_manifest(
        tmp_path / "security",
        plugin_id="security",
        name="Security Plugin",
        version="2.0.0",
    )

    repository = PluginRepository(
        name="Local Plugins",
        url=str(tmp_path),
        repository_type="local",
    )

    discovery = PluginDiscovery()

    packages = discovery.discover(repository)

    assert len(packages) == 2
    assert {
        package.identifier()
        for package in packages
    } == {
        "Calendar Plugin@1.0.0",
        "Security Plugin@2.0.0",
    }


def test_disabled_plugin_descriptor_is_ignored(
    tmp_path: Path,
) -> None:
    """Disabled plugin descriptors should not become packages."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="calendar",
        name="Calendar Plugin",
        version="1.0.0",
        enabled=False,
    )

    repository = PluginRepository(
        name="Local Plugins",
        url=str(tmp_path),
        repository_type="local",
    )

    discovery = PluginDiscovery()

    packages = discovery.discover(repository)

    assert packages == []


def test_disabled_repository_returns_no_plugins(
    tmp_path: Path,
) -> None:
    """Disabled repositories should not be searched."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="calendar",
        name="Calendar Plugin",
        version="1.0.0",
    )

    repository = PluginRepository(
        name="Disabled",
        url=str(tmp_path),
        repository_type="local",
        enabled=False,
    )

    discovery = PluginDiscovery()

    packages = discovery.discover(repository)

    assert packages == []


def test_remote_repository_is_not_loaded_as_local_path() -> None:
    """Remote repositories should await a dedicated adapter."""

    repository = PluginRepository(
        name="FamilyOS Official",
        url="https://plugins.familyos.dev",
        repository_type="official",
    )

    discovery = PluginDiscovery()

    packages = discovery.discover(repository)

    assert packages == []


def test_missing_local_repository_returns_no_plugins(
    tmp_path: Path,
) -> None:
    """Missing local repositories should return no packages."""

    repository = PluginRepository(
        name="Missing",
        url=str(tmp_path / "missing"),
        repository_type="local",
    )

    discovery = PluginDiscovery()

    packages = discovery.discover(repository)

    assert packages == []
