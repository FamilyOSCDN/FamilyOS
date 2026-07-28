"""Tests for runtime dispatch."""

from pathlib import Path

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.domain.models.project import Project
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class DummyPlugin(Plugin):
    """Dummy plugin."""

    metadata = PluginMetadata(
        name="dummy",
        version="1.0.0",
    )

    def __init__(self) -> None:
        self.calls = 0

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        self.calls += 1


def test_runtime_dispatches_hooks() -> None:
    """Runtime should dispatch hooks to active plugins."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)

    context = GenerationContext(
        project=Project(name="demo"),
        destination=Path("demo"),
        variables={
            "project_name": "demo",
        },
    )

    runtime.before_generate(context)

    assert plugin.calls == 1
