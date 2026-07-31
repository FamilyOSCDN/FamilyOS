"""Tests for the plugin resolution pipeline."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.plugins import (
    PluginDiscoveryPort,
)
from familyos_cli.plugins.ecosystem.discovery import (
    PluginDiscovery,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.pipeline import (
    PluginResolutionPipeline,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
    PluginResolver,
)


class FakePluginDiscovery(PluginDiscoveryPort):
    """Return predefined plugin packages."""

    def __init__(
        self,
        packages: list[PluginPackage],
    ) -> None:
        """Initialize fake discovery."""

        self._packages = packages
        self.repository: PluginRepository | None = None

    def discover(
        self,
        repository: PluginRepository,
    ) -> list[PluginPackage]:
        """Return predefined packages."""

        self.repository = repository

        return self._packages


def write_plugin_manifest(
    plugin_directory: Path,
    *,
    plugin_id: str,
    name: str,
    version: str,
) -> None:
    """Write a plugin manifest."""

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
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def test_pipeline_discovers_and_resolves_plugins(
    tmp_path: Path,
) -> None:
    """Pipeline should orchestrate discovery and resolution."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="calendar",
        name="Calendar Plugin",
        version="1.0.0",
    )

    repository = PluginRepository(
        name="Local",
        url=str(tmp_path),
        repository_type="local",
    )

    pipeline = PluginResolutionPipeline(
        discovery=PluginDiscovery(),
        resolver=PluginResolver(),
    )

    plan = pipeline.resolve(
        repository=repository,
        dependencies=[
            PluginDependency(
                name="Calendar Plugin",
            ),
        ],
    )

    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].name == "Calendar Plugin"
    assert plan.diagnostics == []


def test_pipeline_accepts_alternative_discovery_port() -> None:
    """Pipeline should depend on the discovery contract."""

    repository = PluginRepository(
        name="Remote Registry",
        url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    discovery = FakePluginDiscovery(
        packages=[
            PluginPackage(
                name="Calendar Plugin",
                version="2.0.0",
                source="Remote Registry",
            ),
        ],
    )

    pipeline = PluginResolutionPipeline(
        discovery=discovery,
        resolver=PluginResolver(),
    )

    plan = pipeline.resolve(
        repository=repository,
        dependencies=[
            PluginDependency(
                name="Calendar Plugin",
            ),
        ],
    )

    assert discovery.repository is repository
    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].identifier() == (
        "Calendar Plugin@2.0.0"
    )
    assert plan.diagnostics == []
