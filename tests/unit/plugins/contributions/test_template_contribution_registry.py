"""Tests for template contribution registry."""

from pathlib import Path

import pytest

from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
from familyos_cli.plugins.contributions.template_contribution_registry import (
    TemplateContributionRegistry,
)


def test_register_and_list_template_contribution() -> None:
    """Registry should store template contributions."""

    registry = TemplateContributionRegistry()

    contribution = TemplateContribution(
        id=PluginContributionId(
            "familyos.test.template.security",
        ),
        template_directory=Path(
            "templates/security",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.all() == (
        contribution,
    )


def test_register_duplicate_template_directory_fails() -> None:
    """Registry should reject duplicate directories."""

    registry = TemplateContributionRegistry()

    contribution = TemplateContribution(
        id=PluginContributionId(
            "familyos.test.template.security",
        ),
        template_directory=Path(
            "templates/security",
        ),
    )

    registry.register(
        contribution,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            contribution,
        )


def test_get_template_contribution() -> None:
    """Registry should return contribution by directory."""

    registry = TemplateContributionRegistry()

    contribution = TemplateContribution(
        id=PluginContributionId(
            "familyos.test.template.security",
        ),
        template_directory=Path(
            "templates/security",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.get(
        Path(
            "templates/security",
        ),
    ) == contribution


def test_all_returns_registered_templates() -> None:
    """Registry all should return all contributions."""

    registry = TemplateContributionRegistry()

    contribution = TemplateContribution(
        id=PluginContributionId(
            "familyos.test.template.security",
        ),
        template_directory=Path(
            "templates/security",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.all() == (
        contribution,
    )
