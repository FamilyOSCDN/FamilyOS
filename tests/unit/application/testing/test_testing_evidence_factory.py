"""Tests for canonical Testing Framework evidence assembly."""

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
from familyos_cli.application.testing import (
    TestingSourceState as CanonicalTestingSourceState,
)
from familyos_cli.application.testing.testing_evidence_factory import (
    TestingEvidenceFactory,
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


def _source_state() -> CanonicalTestingSourceState:
    return CanonicalTestingSourceState(
        revision="0123456789abcdef0123456789abcdef01234567",
        dirty=False,
    )


def test_factory_preserves_execution_identity() -> None:
    execution_id = _execution_id()

    evidence = TestingEvidenceFactory().create(
        execution_id=execution_id,
        source_state=_source_state(),
        result=_result(),
        captured_at=_captured_at(),
    )

    assert evidence.execution_id == execution_id


def test_factory_uses_captured_source_revision() -> None:
    evidence = TestingEvidenceFactory().create(
        execution_id=_execution_id(),
        source_state=_source_state(),
        result=_result(),
        captured_at=_captured_at(),
    )

    assert evidence.source_revision == (
        "0123456789abcdef0123456789abcdef01234567"
    )


def test_factory_preserves_canonical_result() -> None:
    result = _result()

    evidence = TestingEvidenceFactory().create(
        execution_id=_execution_id(),
        source_state=_source_state(),
        result=result,
        captured_at=_captured_at(),
    )

    assert evidence.result is result


def test_factory_requires_captured_source_revision() -> None:
    source_state = CanonicalTestingSourceState(
        revision=None,
        dirty=None,
    )

    with pytest.raises(
        ValueError,
        match="testing source state does not contain a captured source revision",
    ):
        TestingEvidenceFactory().create(
            execution_id=_execution_id(),
            source_state=source_state,
            result=_result(),
            captured_at=_captured_at(),
        )


def test_factory_does_not_reject_dirty_source_state() -> None:
    source_state = CanonicalTestingSourceState(
        revision="0123456789abcdef0123456789abcdef01234567",
        dirty=True,
    )

    evidence = TestingEvidenceFactory().create(
        execution_id=_execution_id(),
        source_state=source_state,
        result=_result(),
        captured_at=_captured_at(),
    )

    assert evidence.source_revision == source_state.revision
