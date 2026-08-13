"""Tests for the compliance evidence model."""

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_trust_level import (
    EvidenceTrustLevel,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)


def test_compliance_evidence_defaults_to_local_trust() -> None:
    """Evidence defaults to LOCAL trust and a current timestamp."""

    evidence = ComplianceEvidence(
        id="test:0",
        type=EvidenceType.METADATA,
        source="plugin.yaml",
        producer="test.validator",
        producer_version="1.0.0",
        plugin_id="familyos.test",
        plugin_version="1.0.0",
        scope="manifest",
        payload={"key": "value"},
    )

    assert evidence.trust_level is EvidenceTrustLevel.LOCAL
    assert evidence.collected_at is not None
