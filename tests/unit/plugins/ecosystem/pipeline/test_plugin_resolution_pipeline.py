"""Tests for the plugin resolution pipeline."""

from pathlib import Path

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


def write_plugin_manifest(
    plugin_directory: Path,
    *,
    plugin_id: str,
    name: str,
    version: str,
    enabled: bool = True,
) -> None:
    """Write a plugin manifest for pipeline tests."""

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


def test_pipeline_discovers_and_resolves_plugins(
    tmp_path: Path,
) -> None:
    """Pipeline should resolve dependencies by Plugin Identifier."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="familyos.calendar",
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
                plugin_id="familyos.calendar",
            ),
        ],
    )

    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].name == "familyos.calendar"
    assert plan.ordered_packages[0].version == "1.0.0"
    assert plan.ordered_packages[0].identifier() == ("familyos.calendar@1.0.0")
    assert plan.diagnostics == []


def test_pipeline_keeps_plugin_identifier_separate_from_display_name(
    tmp_path: Path,
) -> None:
    """Display name should not participate in dependency resolution."""

    write_plugin_manifest(
        tmp_path / "calendar",
        plugin_id="familyos.calendar",
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
                name="familyos.calendar",
            ),
        ],
    )

    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].name == ("familyos.calendar")
    assert plan.ordered_packages[0].name != "Calendar Plugin"
    assert plan.ordered_packages[0].identifier() == ("familyos.calendar@1.0.0")


def test_pipeline_returns_diagnostic_when_dependency_is_missing(
    tmp_path: Path,
) -> None:
    """Missing dependency should produce a resolution diagnostic."""

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
                name="familyos.missing",
            ),
        ],
    )

    assert plan.ordered_packages == []
    assert len(plan.diagnostics) == 1
    assert plan.diagnostics[0].plugin == "familyos.missing"


def test_pipeline_resolves_highest_compatible_version(
    tmp_path: Path,
) -> None:
    """Pipeline should preserve resolver version selection behavior."""

    resolver = PluginResolver()

    packages = [
        PluginPackage(
            name="familyos.calendar",
            version="1.0.0",
            source="Local",
        ),
        PluginPackage(
            name="familyos.calendar",
            version="1.2.0",
            source="Local",
        ),
    ]

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="familyos.calendar",
                minimum_version="1.0.0",
            ),
        ],
        available_packages=packages,
    )

    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].identifier() == ("familyos.calendar@1.2.0")
