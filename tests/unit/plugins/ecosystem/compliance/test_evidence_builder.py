"""Tests for the compliance evidence builder."""

from familyos_cli.plugins.ecosystem.compliance.evidence_builder import (
    EvidenceBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)


def test_add_accumulates_and_assigns_stable_ids() -> None:
    """Each added evidence item gets a unique, stable id."""

    builder = EvidenceBuilder(
        plugin_id="familyos.test",
        plugin_version="1.0.0",
        producer="test.validator",
    )

    first = builder.add(
        evidence_type=EvidenceType.METADATA,
        source="plugin.yaml",
        scope="manifest",
        payload={"a": 1},
    )
    second = builder.add(
        evidence_type=EvidenceType.METADATA,
        source="plugin.yaml",
        scope="manifest",
        payload={"b": 2},
    )

    assert first.id != second.id
    assert builder.build() == (first, second)
