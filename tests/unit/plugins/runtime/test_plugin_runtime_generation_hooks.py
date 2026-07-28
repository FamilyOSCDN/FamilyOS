"""Tests for generation hooks."""

from pathlib import Path

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.domain.models.project import Project
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class SamplePlugin(Plugin):
    """Sample plugin."""

    metadata = PluginMetadata(
        name="sample",
        version="1.0.0",
    )

    def __init__(self) -> None:
        self.before_called = False
        self.after_called = False

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        self.before_called = True

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        self.after_called = True


def test_runtime_should_dispatch_generation_hooks() -> None:
    """Runtime should dispatch generation hooks."""

    runtime = PluginRuntime()

    plugin = SamplePlugin()

    runtime.activate(plugin)

    context = GenerationContext(
        project=Project(name="demo"),
        destination=Path("demo"),
        variables={
            "project_name": "demo",
        },
    )

    runtime.before_generate(context)
    runtime.after_generate(context)

    assert plugin.before_called
    assert plugin.after_called
