from pathlib import Path

from familyos_cli.plugins.plugin_contribution import (
    PluginContribution,
)


def test_plugin_contribution_defaults() -> None:
    contribution = PluginContribution()

    assert contribution.templates == ()
    assert contribution.specifications == ()
    assert contribution.variables == {}


def test_plugin_contribution_values() -> None:
    contribution = PluginContribution(
        templates=(
            Path("templates"),
        ),
        specifications=(
            Path("specifications"),
        ),
        variables={
            "project": "FamilyOS",
        },
    )

    assert contribution.templates == (
        Path("templates"),
    )

    assert contribution.specifications == (
        Path("specifications"),
    )

    assert contribution.variables == {
        "project": "FamilyOS",
    }