"""Tests for the official compliance profile."""

from familyos_cli.plugins.ecosystem.compliance.profiles.official_profile import (
    OFFICIAL_PROFILE,
)
from familyos_cli.plugins.ecosystem.compliance.rules.default_rule_catalog import (
    DEFAULT_COMPLIANCE_RULES,
)


def test_official_profile_includes_every_default_rule() -> None:
    """The official profile includes every rule tagged for it."""

    assert set(OFFICIAL_PROFILE.included_rule_ids) == {
        rule.id for rule in DEFAULT_COMPLIANCE_RULES
    }


def test_official_profile_marks_namespace_rule_mandatory() -> None:
    """The official profile marks PLUGIN-IDENT-003 mandatory via policy."""

    assert "PLUGIN-IDENT-003" in OFFICIAL_PROFILE.mandatory_rule_ids
