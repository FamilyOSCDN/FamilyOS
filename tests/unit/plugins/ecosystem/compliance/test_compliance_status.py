"""Tests for overall plugin compliance status."""

from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)


def test_compliance_status_values() -> None:
    """Compliance statuses expose stable serialized values."""

    assert ComplianceStatus.COMPLIANT.value == "compliant"
    assert ComplianceStatus.NON_COMPLIANT.value == "non_compliant"
    assert ComplianceStatus.INCOMPLETE.value == "incomplete"
    assert ComplianceStatus.ERROR.value == "error"
