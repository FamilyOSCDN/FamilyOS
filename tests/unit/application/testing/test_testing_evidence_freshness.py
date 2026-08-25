"""Tests for canonical Testing Evidence freshness semantics."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from familyos_cli.application.testing import (
    TestExecutionId as CanonicalExecutionId,
)
from familyos_cli.application.testing import (
    TestExecutionResult as CanonicalExecutionResult,
)
from familyos_cli.application.testing import (
    TestExecutionStatus as CanonicalExecutionStatus,
)
from familyos_cli.application.testing import (
    TestExecutionSummary as CanonicalExecutionSummary,
)
from familyos_cli.application.testing import (
    TestingEvidence as CanonicalTestingEvidence,
)
from familyos_cli.application.testing import (
    TestingSourceState as CanonicalTestingSourceState,
)
from familyos_cli.application.testing.testing_evidence_freshness import (
    TestingEvidenceFreshness as CanonicalEvidenceFreshness,
)
from familyos_cli.application.testing.testing_evidence_freshness import (
    TestingEvidenceFreshnessEvaluator,
)


def _evidence(
    *,
    revision: str = "0123456789abcdef0123456789abcdef01234567",
    dirty: bool = False,
) -> CanonicalTestingEvidence:
    return CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision=revision,
        source_dirty=dirty,
        result=CanonicalExecutionResult(
            status=CanonicalExecutionStatus.PASSED,
            summary=CanonicalExecutionSummary(
                discovered=1,
                executed=1,
                passed=1,
                failed=0,
                skipped=0,
                errors=0,
                duration_seconds=0.1,
            ),
        ),
        captured_at=datetime(
            2026,
            8,
            25,
            8,
            0,
            tzinfo=UTC,
        ),
        native_exit_code=0,
    )


def test_matching_source_state_is_fresh() -> None:
    result = TestingEvidenceFreshnessEvaluator().evaluate(
        evidence=_evidence(),
        current_source_state=CanonicalTestingSourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
    )

    assert result is CanonicalEvidenceFreshness.FRESH


def test_different_revision_is_stale() -> None:
    result = TestingEvidenceFreshnessEvaluator().evaluate(
        evidence=_evidence(),
        current_source_state=CanonicalTestingSourceState(
            revision="fedcba9876543210fedcba9876543210fedcba98",
            dirty=False,
        ),
    )

    assert result is CanonicalEvidenceFreshness.STALE


def test_different_dirty_state_is_stale() -> None:
    result = TestingEvidenceFreshnessEvaluator().evaluate(
        evidence=_evidence(dirty=False),
        current_source_state=CanonicalTestingSourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=True,
        ),
    )

    assert result is CanonicalEvidenceFreshness.STALE


def test_unknown_current_revision_is_unknown() -> None:
    result = TestingEvidenceFreshnessEvaluator().evaluate(
        evidence=_evidence(),
        current_source_state=CanonicalTestingSourceState(
            revision=None,
            dirty=False,
        ),
    )

    assert result is CanonicalEvidenceFreshness.UNKNOWN


def test_unknown_current_dirty_state_is_unknown() -> None:
    result = TestingEvidenceFreshnessEvaluator().evaluate(
        evidence=_evidence(),
        current_source_state=CanonicalTestingSourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=None,
        ),
    )

    assert result is CanonicalEvidenceFreshness.UNKNOWN
