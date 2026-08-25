"""Tests for Testing Evidence propagation through CI validation."""

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
from familyos_cli.application.validation import (
    GateResult,
    ValidationStatus,
)


def test_gate_result_can_retain_testing_evidence() -> None:
    """Retain Testing-owned evidence without redefining its semantics."""

    evidence = CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision=(
            "0123456789abcdef0123456789abcdef01234567"
        ),
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
            7,
            30,
            tzinfo=UTC,
        ),
        native_exit_code=0,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.PASSED,
        exit_code=0,
        testing_evidence=evidence,
    )

    assert gate.testing_evidence is evidence
    assert gate.testing_evidence.execution_id is evidence.execution_id
    assert gate.testing_evidence.source_revision == evidence.source_revision
    assert gate.testing_evidence.captured_at == evidence.captured_at
