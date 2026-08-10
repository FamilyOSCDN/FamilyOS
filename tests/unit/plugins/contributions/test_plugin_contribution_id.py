"""Tests for canonical plugin contribution identifiers."""

import pytest

from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


@pytest.mark.parametrize(
    "value",
    [
        "familyos.security.generation",
        "familyos.education.recipe.documentation",
        "familyos.documents.templates",
        "acme.backup.archive",
        "acme.backup.recipe.full",
    ],
)
def test_plugin_contribution_id_accepts_canonical_syntax(
    value: str,
) -> None:
    """Canonical contribution identifiers should be accepted."""

    contribution_id = PluginContributionId(value)

    assert contribution_id.value == value
    assert str(contribution_id) == value


def test_plugin_contribution_id_rejects_empty_value() -> None:
    """Contribution identifiers should reject empty values."""

    with pytest.raises(
        ValueError,
        match="Plugin contribution id cannot be empty.",
    ):
        PluginContributionId("")


@pytest.mark.parametrize(
    "value",
    [
        "generation",
        "security.generation",
        "FamilyOS.security.generation",
        "familyos security generation",
        ".familyos.security.generation",
        "familyos.security.generation.",
        "familyos..security.generation",
        "familyos.security",
    ],
)
def test_plugin_contribution_id_rejects_invalid_syntax(
    value: str,
) -> None:
    """Contribution identifiers should require canonical syntax."""

    with pytest.raises(
        ValueError,
        match="Invalid plugin contribution id",
    ):
        PluginContributionId(value)
