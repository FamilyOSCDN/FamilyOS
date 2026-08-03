from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
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


def activate_health_plugin() -> PluginRuntime:
    """Activate health plugin in runtime."""

    runtime = PluginRuntime()

    runtime.activate(
        HealthPlugin(),
    )

    return runtime


def test_health_plugin_registers_generation_contribution() -> None:
    runtime = activate_health_plugin()

    contributions = (
        runtime.generation_contributions()
    )

    assert len(contributions) == 1

    contribution = contributions[0]

    assert isinstance(
        contribution,
        GenerationContribution,
    )

    assert str(
        contribution.preset,
    ) == "health"


def test_health_plugin_registers_recipe_contribution() -> None:
    runtime = activate_health_plugin()

    contributions = (
        runtime.generation_recipe_contributions()
    )

    assert len(contributions) == 1

    contribution = contributions[0]

    assert isinstance(
        contribution,
        GenerationRecipeContribution,
    )

    assert (
        contribution.recipe.name
        == "health_documentation"
    )


def test_health_plugin_registers_template_contribution() -> None:
    runtime = activate_health_plugin()

    contributions = (
        runtime.template_contributions()
    )

    assert len(contributions) == 1

    contribution = contributions[0]

    assert isinstance(
        contribution,
        TemplateContribution,
    )

    assert (
        contribution.template_directory.name
        == "health"
    )
