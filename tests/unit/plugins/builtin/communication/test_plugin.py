"""Tests for CommunicationPlugin."""

from pathlib import Path

from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
from familyos_cli.plugins.models import (
    PluginMetadata,
)


def test_communication_plugin_metadata() -> None:
    plugin = CommunicationPlugin()

    metadata = plugin.get_metadata()

    assert isinstance(
        metadata,
        PluginMetadata,
    )

    assert metadata.name == (
        "FamilyOS Communication Plugin"
    )

    assert metadata.version == "1.0.0"

    assert metadata.author == (
        "FamilyOS Team"
    )


def test_communication_plugin_description() -> None:
    plugin = CommunicationPlugin()

    metadata = plugin.get_metadata()

    assert (
        "communication management"
        in metadata.description
    )

    assert (
        "communication archive"
        in metadata.description
    )


def test_communication_plugin_provides_capabilities() -> None:
    plugin = CommunicationPlugin()

    capabilities = plugin.capabilities()

    assert len(capabilities) == 2

    assert [
        str(capability.id)
        for capability in capabilities
    ] == [
        "familyos.communication.messaging",
        "familyos.communication.archive",
    ]


def test_communication_plugin_provides_generation_contributions() -> None:
    plugin = CommunicationPlugin()

    contributions = plugin.contributions()

    assert len(contributions) == 3

    assert isinstance(
        contributions[0],
        GenerationContribution,
    )

    assert isinstance(
        contributions[1],
        GenerationRecipeContribution,
    )

    assert isinstance(
        contributions[2],
        TemplateContribution,
    )


def test_communication_plugin_exposes_communication_preset() -> None:
    plugin = CommunicationPlugin()

    contribution = plugin.contributions()[0]

    assert isinstance(
        contribution,
        GenerationContribution,
    )

    assert str(contribution.preset) == (
        "communication"
    )

    assert contribution.recipes == (
        "communication-documentation",
    )


def test_communication_plugin_exposes_documentation_recipe() -> None:
    plugin = CommunicationPlugin()

    contribution = plugin.contributions()[1]

    assert isinstance(
        contribution,
        GenerationRecipeContribution,
    )

    assert contribution.recipe.name == (
        "communication-documentation"
    )


def test_communication_plugin_exposes_template_directory() -> None:
    plugin = CommunicationPlugin()

    contribution = plugin.contributions()[2]

    assert isinstance(
        contribution,
        TemplateContribution,
    )

    expected_directory = (
        Path(__file__)
        .parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "communication"
        / "templates"
    )

    assert (
        contribution.template_directory.resolve()
        == expected_directory.resolve()
    )
