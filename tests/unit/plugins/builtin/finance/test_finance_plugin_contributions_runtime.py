from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
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


def activate_finance_plugin() -> PluginRuntime:
    """Activate finance plugin."""

    runtime = PluginRuntime()

    runtime.activate(
        FinancePlugin(),
    )

    return runtime


def test_finance_plugin_registers_generation_contribution() -> None:
    runtime = activate_finance_plugin()

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
    ) == "finance"


def test_finance_plugin_registers_recipe_contribution() -> None:
    runtime = activate_finance_plugin()

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
        == "finance_documentation"
    )


def test_finance_plugin_registers_template_contribution() -> None:
    runtime = activate_finance_plugin()

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
        == "finance"
    )
