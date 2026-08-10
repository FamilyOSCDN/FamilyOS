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
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def activate_communication_plugin() -> PluginRuntime:
    """Activate communication plugin."""

    runtime = PluginRuntime()

    runtime.activate(
        CommunicationPlugin(),
    )

    return runtime


def test_communication_plugin_registers_generation_contribution() -> None:
    runtime = activate_communication_plugin()

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
    ) == "communication"

    assert contributions[0].recipes == (
        "communication-documentation",
    )


def test_communication_plugin_registers_recipe_contribution() -> None:
    runtime = activate_communication_plugin()

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
        == "communication-documentation"
    )


def test_communication_plugin_registers_template_contribution() -> None:
    runtime = activate_communication_plugin()

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
