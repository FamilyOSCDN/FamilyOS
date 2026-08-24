"""Tests for canonical Testing Evidence timestamp semantics."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

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
from familyos_cli.application.testing.testing_evidence import (
    TestingEvidence as CanonicalTestingEvidence,
)


def _execution_id() -> CanonicalExecutionId:
    return CanonicalExecutionId(
        UUID("01234567-89ab-cdef-0123-456789abcdef")
    )


def _result() -> CanonicalExecutionResult:
    return CanonicalExecutionResult(
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
    )


def _captured_at() -> datetime:
    return datetime(
        2026,
        8,
        24,
        19,
        45,
        tzinfo=UTC,
    )


def test_evidence_preserves_captured_timestamp() -> None:
    captured_at = _captured_at()

    evidence = CanonicalTestingEvidence(
        execution_id=_execution_id(),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        result=_result(),
        captured_at=captured_at,
    )

    assert evidence.captured_at == captured_at


def test_evidence_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(
        ValueError,
        match="Testing Evidence timestamp must be timezone-aware",
    ):
        CanonicalTestingEvidence(
            execution_id=_execution_id(),
            source_revision="0123456789abcdef0123456789abcdef01234567",
            result=_result(),
            captured_at=datetime(2026, 8, 24, 19, 45),
        )


def test_evidence_timestamp_is_immutable() -> None:
    evidence = CanonicalTestingEvidence(
        execution_id=_execution_id(),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        result=_result(),
        captured_at=_captured_at(),
    )

    with pytest.raises(AttributeError):
        evidence.captured_at = datetime.now(UTC)  # type: ignore[misc]
