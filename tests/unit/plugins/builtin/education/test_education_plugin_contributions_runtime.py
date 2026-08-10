from familyos_cli.plugins.builtin.education.plugin import (
    EducationPlugin,
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


def activate_education_plugin() -> PluginRuntime:
    """Activate education plugin."""

    runtime = PluginRuntime()

    runtime.activate(
        EducationPlugin(),
    )

    return runtime


def test_education_plugin_registers_generation_contribution() -> None:
    runtime = activate_education_plugin()

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
    ) == "education"

    assert contributions[0].recipes == (
        "education-domain",
        "education-documentation",
    )


def test_education_plugin_registers_recipe_contributions() -> None:
    runtime = activate_education_plugin()

    contributions = (
        runtime.generation_recipe_contributions()
    )

    assert len(contributions) == 2

    assert all(
        isinstance(
            contribution,
            GenerationRecipeContribution,
        )
        for contribution in contributions
    )

    assert [
        contribution.recipe.name
        for contribution in contributions
    ] == [
        "education-domain",
        "education-documentation",
    ]


def test_education_plugin_registers_template_contribution() -> None:
    runtime = activate_education_plugin()

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
