"""Tests for Testing Evidence projection in canonical CI JSON."""

from __future__ import annotations

import json
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
    CiValidationResult,
    GateResult,
    ValidationStatus,
)
from familyos_cli.interfaces.cli.rendering.ci_validation_json import (
    CiValidationJsonRenderer,
)


def test_renderer_projects_testing_evidence_for_pytest_gate() -> None:
    evidence = CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision=(
            "0123456789abcdef0123456789abcdef01234567"
        ),
        source_dirty=False,
        result=CanonicalExecutionResult(
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

    result = CiValidationResult(
        gates=(
            GateResult(
                gate_id="pytest",
                status=ValidationStatus.PASSED,
                exit_code=0,
                testing_evidence=evidence,
            ),
        ),
    )

    payload = json.loads(
        CiValidationJsonRenderer().render(result)
    )

    gate = payload["gates"][0]

    assert gate["testing_evidence"] == {
        "execution_id": "01234567-89ab-cdef-0123-456789abcdef",
        "source_revision": (
            "0123456789abcdef0123456789abcdef01234567"
        ),
        "captured_at": "2026-08-25T07:30:00+00:00",
        "native_exit_code": 0,
        "result": {
            "status": "passed",
            "summary": {
                "discovered": 3,
                "executed": 3,
                "passed": 3,
                "failed": 0,
                "skipped": 0,
                "errors": 0,
                "duration_seconds": 0.25,
            },
            "diagnostic": None,
        },
    }


def test_renderer_omits_testing_evidence_for_non_testing_gate() -> None:
    result = CiValidationResult(
        gates=(
            GateResult(
                gate_id="ruff",
                status=ValidationStatus.PASSED,
                exit_code=0,
            ),
        ),
    )

    payload = json.loads(
        CiValidationJsonRenderer().render(result)
    )

    assert "testing_evidence" not in payload["gates"][0]
