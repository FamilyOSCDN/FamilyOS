"""Tests for the base plugin contract."""

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.plugins.plugin import Plugin


class DummyPlugin(Plugin):
    """Dummy plugin."""


def test_plugin_has_default_hooks() -> None:
    """Base plugins should expose safe default hooks."""

    plugin = DummyPlugin()

    context = GenerationContext(
        variables={
            "project_name": "demo",
            "output_directory": "/tmp/demo",
        },
    )

    plugin.before_generate(
        context,
    )

    plugin.after_generate(
        context,
    )


def test_plugin_has_no_capabilities_by_default() -> None:
    """Base plugins should expose no capabilities."""

    plugin = DummyPlugin()

    assert plugin.capabilities() == ()
