"""Compliance evidence model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from familyos_cli.plugins.ecosystem.compliance.evidence_trust_level import (
    EvidenceTrustLevel,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)


@dataclass(frozen=True, slots=True)
class ComplianceEvidence:
    """Represent one normalized observation supporting rule evaluation.

    See docs/epics/EPIC-PLUGIN-002-plugin-compliance-framework/
    09-Evidence-Model.md for the full conceptual model.
    """

    id: str
    type: EvidenceType
    source: str
    producer: str
    producer_version: str
    plugin_id: str
    plugin_version: str
    scope: str
    payload: Mapping[str, Any]
    trust_level: EvidenceTrustLevel = EvidenceTrustLevel.LOCAL
    collected_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
