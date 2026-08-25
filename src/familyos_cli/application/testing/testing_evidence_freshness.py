"""Canonical Testing Evidence freshness semantics."""

from __future__ import annotations

from enum import StrEnum

from familyos_cli.application.testing.testing_evidence import TestingEvidence
from familyos_cli.application.testing.testing_source_state import (
    TestingSourceState,
)


class TestingEvidenceFreshness(StrEnum):
    """Freshness classification for canonical Testing Evidence."""

    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"


class TestingEvidenceFreshnessEvaluator:
    """Compare Testing Evidence with the currently observed source state."""

    def evaluate(
        self,
        *,
        evidence: TestingEvidence,
        current_source_state: TestingSourceState,
    ) -> TestingEvidenceFreshness:
        """Return canonical evidence freshness for the current source state."""

        if (
            current_source_state.revision is None
            or current_source_state.dirty is None
        ):
            return TestingEvidenceFreshness.UNKNOWN

        if (
            evidence.source_revision != current_source_state.revision
            or evidence.source_dirty != current_source_state.dirty
        ):
            return TestingEvidenceFreshness.STALE

        return TestingEvidenceFreshness.FRESH
