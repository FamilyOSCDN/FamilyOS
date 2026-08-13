"""Tests for the compliance profile model."""

from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity


def test_compliance_profile_defaults() -> None:
    """A ComplianceProfile defaults to an ERROR blocking threshold."""

    profile = ComplianceProfile(
        id="test",
        version="1.0.0",
        description="Test profile.",
        included_rule_ids=("PLUGIN-TEST-001",),
    )

    assert profile.excluded_rule_ids == ()
    assert profile.mandatory_rule_ids == ()
    assert profile.blocking_severity_threshold is Severity.ERROR
