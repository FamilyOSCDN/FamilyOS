"""Tests for canonical Testing Framework evidence."""

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


def _captured_at() -> datetime:
    return datetime(
        2026,
        8,
        24,
        19,
        45,
        tzinfo=UTC,
    )


def _result() -> CanonicalExecutionResult:
    return CanonicalExecutionResult(
        status=CanonicalExecutionStatus.PASSED,
        summary=CanonicalExecutionSummary(
            discovered=3,
            executed=3,
            passed=3,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=0.25,
        ),
    )


def test_evidence_preserves_execution_identity() -> None:
    evidence = CanonicalTestingEvidence(
        execution_id=_execution_id(),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        result=_result(),
        captured_at=_captured_at(),
    )

    assert evidence.execution_id == _execution_id()


def test_evidence_preserves_source_revision() -> None:
    revision = "0123456789abcdef0123456789abcdef01234567"

    evidence = CanonicalTestingEvidence(
        execution_id=_execution_id(),
        source_revision=revision,
        result=_result(),
        captured_at=_captured_at(),
    )

    assert evidence.source_revision == revision


def test_evidence_preserves_canonical_result() -> None:
    result = _result()

    evidence = CanonicalTestingEvidence(
        execution_id=_execution_id(),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        result=result,
        captured_at=_captured_at(),
    )

    assert evidence.result is result


def test_evidence_requires_source_revision() -> None:
    with pytest.raises(
        ValueError,
        match="Testing Evidence requires a source revision",
    ):
        CanonicalTestingEvidence(
            execution_id=_execution_id(),
            source_revision="",
            result=_result(),
            captured_at=_captured_at(),
        )


def test_evidence_is_immutable() -> None:
    evidence = CanonicalTestingEvidence(
        execution_id=_execution_id(),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        result=_result(),
        captured_at=_captured_at(),
    )

    with pytest.raises(AttributeError):
        evidence.source_revision = "replacement"  # type: ignore[misc]
