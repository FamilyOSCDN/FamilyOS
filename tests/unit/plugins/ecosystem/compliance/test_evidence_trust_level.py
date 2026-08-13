"""Tests for compliance evidence trust levels."""

from familyos_cli.plugins.ecosystem.compliance.evidence_trust_level import (
    EvidenceTrustLevel,
)


def test_evidence_trust_level_values() -> None:
    """Evidence trust levels expose stable serialized values."""

    assert EvidenceTrustLevel.UNVERIFIED.value == "unverified"
    assert EvidenceTrustLevel.LOCAL.value == "local"
    assert EvidenceTrustLevel.TRUSTED.value == "trusted"
    assert EvidenceTrustLevel.ATTESTED.value == "attested"
