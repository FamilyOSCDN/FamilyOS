from inspect import getfile
from pathlib import Path

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


def test_education_plugin_provides_generation_contributions() -> None:
    plugin = EducationPlugin()

    contributions = plugin.contributions()

    assert any(
        isinstance(
            contribution,
            GenerationContribution,
        )
        for contribution in contributions
    )


def test_education_plugin_provides_recipe_contributions() -> None:
    plugin = EducationPlugin()

    contributions = plugin.contributions()

    recipes = [
        contribution
        for contribution in contributions
        if isinstance(
            contribution,
            GenerationRecipeContribution,
        )
    ]

    assert len(recipes) == 2


def test_education_plugin_provides_template_contribution() -> None:
    plugin = EducationPlugin()

    contributions = plugin.contributions()

    templates = [
        contribution
        for contribution in contributions
        if isinstance(
            contribution,
            TemplateContribution,
        )
    ]

    assert len(templates) == 1


def test_education_template_contribution_targets_template_directory() -> None:
    plugin = EducationPlugin()

    contributions = plugin.contributions()

    template_contribution = next(
        contribution
        for contribution in contributions
        if isinstance(
            contribution,
            TemplateContribution,
        )
    )

    expected_directory = (
        Path(getfile(EducationPlugin)).parent
        / "templates"
    )

    assert (
        template_contribution.template_directory
        == expected_directory
    )
    assert template_contribution.template_directory.is_dir()


def test_education_plugin_contribution_order_is_deterministic() -> None:
    plugin = EducationPlugin()

    contributions = plugin.contributions()

    assert len(contributions) == 4
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
        GenerationRecipeContribution,
    )
    assert isinstance(
        contributions[3],
        TemplateContribution,
    )
