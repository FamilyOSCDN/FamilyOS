"""Tests for rule applicability."""

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)


def test_empty_applicability_applies_to_every_classification() -> None:
    """An empty classifications tuple applies to every classification."""

    applicability = RuleApplicability()

    assert applicability.applies_to(PluginClassification.OFFICIAL)
    assert applicability.applies_to(PluginClassification.THIRD_PARTY)


def test_scoped_applicability_applies_only_to_listed_classifications() -> None:
    """A scoped applicability applies only to its listed classifications."""

    applicability = RuleApplicability(
        classifications=(PluginClassification.OFFICIAL,),
    )

    assert applicability.applies_to(PluginClassification.OFFICIAL)
    assert not applicability.applies_to(PluginClassification.THIRD_PARTY)
