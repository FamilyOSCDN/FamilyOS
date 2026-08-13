"""Compliance evidence accumulator."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)


@dataclass(slots=True)
class EvidenceBuilder:
    """Accumulate normalized evidence produced by a single validator run."""

    plugin_id: str
    plugin_version: str
    producer: str
    producer_version: str = "1.0.0"
    _evidence: list[ComplianceEvidence] = field(default_factory=list)

    def add(
        self,
        *,
        evidence_type: EvidenceType,
        source: str,
        scope: str,
        payload: Mapping[str, Any],
    ) -> ComplianceEvidence:
        """Record one evidence item and return it."""

        evidence = ComplianceEvidence(
            id=f"{self.producer}:{len(self._evidence)}",
            type=evidence_type,
            source=source,
            producer=self.producer,
            producer_version=self.producer_version,
            plugin_id=self.plugin_id,
            plugin_version=self.plugin_version,
            scope=scope,
            payload=payload,
        )

        self._evidence.append(evidence)

        return evidence

    def build(self) -> tuple[ComplianceEvidence, ...]:
        """Return the accumulated evidence as an immutable tuple."""

        return tuple(self._evidence)
