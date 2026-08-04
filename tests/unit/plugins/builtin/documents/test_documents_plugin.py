from pathlib import Path

from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
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


def test_documents_plugin_metadata() -> None:
    plugin = DocumentsPlugin()

    metadata = plugin.get_metadata()

    assert isinstance(
        metadata,
        PluginMetadata,
    )

    assert metadata.name == (
        "FamilyOS Documents Plugin"
    )

    assert metadata.version == "1.0.0"

    assert metadata.author == (
        "FamilyOS Team"
    )


def test_documents_plugin_description() -> None:
    plugin = DocumentsPlugin()

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert (
        "document management"
        in metadata.description
    )

    assert (
        "family digital archive"
        in metadata.description
    )


def test_documents_plugin_provides_capabilities() -> None:
    plugin = DocumentsPlugin()

    capabilities = plugin.capabilities()

    assert len(capabilities) == 2

    assert [
        str(capability.id)
        for capability in capabilities
    ] == [
        "familyos.documents.document",
        "familyos.documents.archive",
    ]


def test_documents_plugin_provides_generation_contributions() -> None:
    plugin = DocumentsPlugin()

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


def test_documents_plugin_exposes_documents_preset() -> None:
    plugin = DocumentsPlugin()

    contribution = plugin.contributions()[0]

    assert isinstance(
        contribution,
        GenerationContribution,
    )

    assert str(contribution.preset) == (
        "documents"
    )

    assert contribution.recipes == (
        "documents-documentation",
    )


def test_documents_plugin_exposes_documentation_recipe() -> None:
    plugin = DocumentsPlugin()

    contribution = plugin.contributions()[1]

    assert isinstance(
        contribution,
        GenerationRecipeContribution,
    )

    assert contribution.recipe.name == (
        "documents-documentation"
    )


def test_documents_plugin_exposes_template_directory() -> None:
    plugin = DocumentsPlugin()

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
        / "documents"
        / "templates"
    )

    assert (
        contribution.template_directory.resolve()
        == expected_directory.resolve()
    )
