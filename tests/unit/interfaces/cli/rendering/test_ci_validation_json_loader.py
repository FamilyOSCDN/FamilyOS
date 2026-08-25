"""Tests for canonical CI validation JSON loading."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import UUID

import pytest

from familyos_cli.application.testing import (
    TestExecutionId as CanonicalTestExecutionId,
)
from familyos_cli.application.testing import (
    TestExecutionStatus as CanonicalTestExecutionStatus,
)
from familyos_cli.application.validation import (
    CI_VALIDATION_SCHEMA_VERSION,
    ValidationStatus,
)
from familyos_cli.interfaces.cli.rendering.ci_validation_json_loader import (
    CiValidationJsonLoader,
)


def _payload() -> dict[str, object]:
    return {
        "schema_version": CI_VALIDATION_SCHEMA_VERSION,
        "profile": "ci",
        "status": "passed",
        "gates": [
            {
                "id": "pytest",
                "status": "passed",
                "exit_code": 0,
                "diagnostic": None,
                "testing_evidence": {
                    "execution_id": (
                        "01234567-89ab-cdef-0123-456789abcdef"
                    ),
                    "source_revision": (
                        "0123456789abcdef0123456789abcdef01234567"
                    ),
                    "source_dirty": False,
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
                },
            }
        ],
    }


def test_loader_reconstructs_canonical_pytest_testing_authority() -> None:
    result = CiValidationJsonLoader().load(
        json.dumps(_payload())
    )

    assert result.schema_version == CI_VALIDATION_SCHEMA_VERSION
    assert result.profile == "ci"
    assert result.status is ValidationStatus.PASSED
    assert len(result.gates) == 1

    gate = result.gates[0]

    assert gate.gate_id == "pytest"
    assert gate.status is ValidationStatus.PASSED
    assert gate.exit_code == 0
    assert gate.diagnostic is None

    evidence = gate.testing_evidence

    assert evidence is not None
    assert evidence.execution_id == CanonicalTestExecutionId(
        UUID("01234567-89ab-cdef-0123-456789abcdef")
    )
    assert evidence.source_revision == (
        "0123456789abcdef0123456789abcdef01234567"
    )
    assert evidence.source_dirty is False
    assert evidence.captured_at == datetime(
        2026,
        8,
        25,
        7,
        30,
        tzinfo=UTC,
    )
    assert evidence.native_exit_code == 0

    assert evidence.result.status is CanonicalTestExecutionStatus.PASSED
    assert evidence.result.summary.discovered == 3
    assert evidence.result.summary.executed == 3
    assert evidence.result.summary.passed == 3
    assert evidence.result.summary.failed == 0
    assert evidence.result.summary.skipped == 0
    assert evidence.result.summary.errors == 0
    assert evidence.result.summary.duration_seconds == 0.25
    assert evidence.result.diagnostic is None


def test_loader_rejects_unsupported_schema_version() -> None:
    payload = _payload()
    payload["schema_version"] = "999.0.0"

    with pytest.raises(
        ValueError,
        match="unsupported CI validation schema version",
    ):
        CiValidationJsonLoader().load(
            json.dumps(payload)
        )


def test_loader_requires_pytest_source_dirty() -> None:
    payload = _payload()

    gates = payload["gates"]
    assert isinstance(gates, list)

    gate = gates[0]
    assert isinstance(gate, dict)

    evidence = gate["testing_evidence"]
    assert isinstance(evidence, dict)

    del evidence["source_dirty"]

    with pytest.raises(
        ValueError,
        match="testing evidence source_dirty is required",
    ):
        CiValidationJsonLoader().load(
            json.dumps(payload)
        )


def test_renderer_loader_round_trip_preserves_pytest_authority() -> None:
    from familyos_cli.application.testing import (
        TestExecutionResult as CanonicalTestExecutionResult,
    )
    from familyos_cli.application.testing import (
        TestExecutionSummary as CanonicalTestExecutionSummary,
    )
    from familyos_cli.application.testing import (
        TestingEvidence,
    )
    from familyos_cli.application.validation import (
        CiValidationResult,
        GateResult,
    )
    from familyos_cli.interfaces.cli.rendering.ci_validation_json import (
        CiValidationJsonRenderer,
    )

    testing_evidence = TestingEvidence(
        execution_id=CanonicalTestExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision=(
            "0123456789abcdef0123456789abcdef01234567"
        ),
        source_dirty=False,
        result=CanonicalTestExecutionResult(
            status=CanonicalTestExecutionStatus.PASSED,
            summary=CanonicalTestExecutionSummary(
                discovered=1725,
                executed=1725,
                passed=1725,
                failed=0,
                skipped=0,
                errors=0,
                duration_seconds=42.5,
            ),
        ),
        captured_at=datetime(
            2026,
            8,
            25,
            19,
            30,
            tzinfo=UTC,
        ),
        native_exit_code=0,
    )

    original = CiValidationResult(
        gates=(
            GateResult(
                gate_id="pytest",
                status=ValidationStatus.PASSED,
                exit_code=0,
                testing_evidence=testing_evidence,
            ),
        ),
    )

    rendered = CiValidationJsonRenderer().render(original)
    reconstructed = CiValidationJsonLoader().load(rendered)

    assert reconstructed.schema_version == original.schema_version
    assert reconstructed.profile == original.profile
    assert reconstructed.status is original.status

    assert len(reconstructed.gates) == 1

    gate = reconstructed.gates[0]

    assert gate.gate_id == "pytest"
    assert gate.status is ValidationStatus.PASSED
    assert gate.exit_code == 0
    assert gate.diagnostic is None

    evidence = gate.testing_evidence

    assert evidence is not None
    assert evidence.execution_id == testing_evidence.execution_id
    assert evidence.source_revision == testing_evidence.source_revision
    assert evidence.source_dirty is testing_evidence.source_dirty
    assert evidence.captured_at == testing_evidence.captured_at
    assert evidence.native_exit_code == testing_evidence.native_exit_code

    assert evidence.result.status is testing_evidence.result.status
    assert evidence.result.summary == testing_evidence.result.summary
    assert evidence.result.diagnostic == testing_evidence.result.diagnostic
