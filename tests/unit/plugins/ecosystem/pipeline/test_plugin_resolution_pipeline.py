"""Tests for the plugin resolution pipeline."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.discovery import (
    PluginDiscovery,
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
