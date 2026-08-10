from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
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


def activate_security_plugin() -> PluginRuntime:
    """Activate security plugin in runtime."""

    runtime = PluginRuntime()

    runtime.activate(
        SecurityPlugin(),
        plugin_id="familyos.security",
    )

    return runtime


def test_security_plugin_registers_generation_contribution() -> None:
    runtime = activate_security_plugin()

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
    ) == "security"


def test_security_plugin_registers_recipe_contribution() -> None:
    runtime = activate_security_plugin()

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
        == "security_documentation"
    )


def test_security_plugin_registers_template_contribution() -> None:
    runtime = activate_security_plugin()

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
        == "security"
    )
