"""Tests for compliance evidence types."""

from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)


def test_evidence_type_values() -> None:
    """Evidence types expose stable serialized values."""

    assert EvidenceType.IDENTITY.value == "identity"
    assert EvidenceType.METADATA.value == "metadata"
    assert EvidenceType.STRUCTURE.value == "structure"
    assert EvidenceType.ARCHITECTURE.value == "architecture"
    assert EvidenceType.CAPABILITY.value == "capability"
    assert EvidenceType.DEPENDENCY.value == "dependency"
    assert EvidenceType.QUALITY.value == "quality"
