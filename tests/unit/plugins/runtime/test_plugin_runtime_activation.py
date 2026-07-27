"""Tests for plugin activation."""

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
        name="Dummy Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Dummy plugin",
    )

    def __init__(self) -> None:
        self.called = False

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        self.called = True


def test_activate_plugin_dispatches_hook() -> None:
    """Activated plugins should receive generation hooks."""

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

    assert plugin.called