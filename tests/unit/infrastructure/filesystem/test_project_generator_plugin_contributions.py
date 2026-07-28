"""Tests for ProjectGenerator plugin contributions."""

from pathlib import Path

from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_contribution import PluginContribution
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class BlogPlugin(Plugin):
    """Fake plugin."""

    def contribution(self) -> PluginContribution:
        return PluginContribution(
            templates=(Path("plugins/blog/templates"),),
            specifications=(Path("plugins/blog/specifications/project.yaml"),),
        )


def test_should_collect_plugin_contributions() -> None:
    """ProjectGenerator should expose plugin contributions."""

    runtime = PluginRuntime()

    runtime.activate(
        BlogPlugin(),
    )

    generator = ProjectGenerator(
        runtime=runtime,
    )

    assert generator.plugin_contributions.templates == (Path("plugins/blog/templates"),)

    assert generator.plugin_contributions.specifications == (
        Path("plugins/blog/specifications/project.yaml"),
    )
