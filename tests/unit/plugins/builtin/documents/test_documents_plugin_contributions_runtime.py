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
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def activate_documents_plugin() -> PluginRuntime:
    """Activate documents plugin."""

    runtime = PluginRuntime()

    runtime.activate(
        DocumentsPlugin(),
        plugin_id="familyos.documents",
    )

    return runtime


def test_documents_plugin_registers_generation_contribution() -> None:
    runtime = activate_documents_plugin()

    contributions = (
        runtime.generation_contributions()
    )

    assert len(contributions) == 1

    assert isinstance(
        contributions[0],
        GenerationContribution,
    )

    assert str(
        contributions[0].preset,
    ) == "documents"

    assert contributions[0].recipes == (
        "documents-documentation",
    )


def test_documents_plugin_registers_recipe_contribution() -> None:
    runtime = activate_documents_plugin()

    contributions = (
        runtime.generation_recipe_contributions()
    )

    assert len(contributions) == 1

    assert isinstance(
        contributions[0],
        GenerationRecipeContribution,
    )

    assert (
        contributions[0].recipe.name
        == "documents-documentation"
    )


def test_documents_plugin_registers_template_contribution() -> None:
    runtime = activate_documents_plugin()

    contributions = (
        runtime.template_contributions()
    )

    assert len(contributions) == 1

    assert isinstance(
        contributions[0],
        TemplateContribution,
    )

    assert (
        contributions[0]
        .template_directory
        .name
        == "templates"
    )