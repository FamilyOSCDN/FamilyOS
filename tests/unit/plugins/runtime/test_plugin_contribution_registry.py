"""Tests for PluginContributionRegistry."""

from pathlib import Path

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_contribution import PluginContribution
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_contribution_registry import (
    PluginContributionRegistry,
)


class DummyPlugin(Plugin):
    """Dummy plugin."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Dummy",
            version="1.0.0",
        )

    def contribution(self) -> PluginContribution:
        return PluginContribution(
            templates=(Path("templates"),),
            specifications=(Path("specifications"),),
            variables={
                "project": "FamilyOS",
            },
        )


def test_should_register_plugin_contribution() -> None:
    """Registry should collect plugin contributions."""

    registry = PluginContributionRegistry()

    registry.register(
        DummyPlugin(),
    )

    contributions = registry.all()

    assert len(contributions) == 1

    assert contributions[0].variables == {
        "project": "FamilyOS",
    }
