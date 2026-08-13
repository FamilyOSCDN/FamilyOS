"""Tests for compliance rule domains."""

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)


def test_compliance_domain_values() -> None:
    """Compliance domains expose stable serialized values."""

    assert ComplianceDomain.IDENTITY.value == "identity"
    assert ComplianceDomain.METADATA.value == "metadata"
    assert ComplianceDomain.STRUCTURE.value == "structure"
    assert ComplianceDomain.ARCHITECTURE.value == "architecture"
    assert ComplianceDomain.CAPABILITIES.value == "capabilities"
    assert ComplianceDomain.DEPENDENCIES.value == "dependencies"
