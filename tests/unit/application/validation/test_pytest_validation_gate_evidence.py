"""Tests for canonical pytest validation from Testing Evidence."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from familyos_cli.application.ports.testing import (
    TestingEvidenceFreshnessPort,
    TestingExecutionPort,
)
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
from familyos_cli.application.testing.testing_evidence_freshness import (
    TestingEvidenceFreshness as CanonicalEvidenceFreshness,
)
from familyos_cli.application.validation import ValidationStatus
from familyos_cli.application.validation.pytest_validation_gate import (
    PytestValidationGate,
)


class _AlwaysFresh(TestingEvidenceFreshnessPort):
    def evaluate(
        self,
        *,
        project_root: Path,
        evidence: CanonicalTestingEvidence,
    ) -> CanonicalEvidenceFreshness:
        return CanonicalEvidenceFreshness.FRESH


class _EvidenceExecution(TestingExecutionPort):
    def __init__(
        self,
        evidence: CanonicalTestingEvidence,
    ) -> None:
        self.evidence = evidence
        self.project_root: Path | None = None
        self.test_paths: tuple[Path, ...] | None = None

    def execute(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> CanonicalTestingEvidence:
        self.project_root = project_root
        self.test_paths = test_paths
        return self.evidence


def _evidence(
    status: CanonicalExecutionStatus,
    *,
    diagnostic: str | None = None,
) -> CanonicalTestingEvidence:
    summary = CanonicalExecutionSummary(
        discovered=1,
        executed=1,
        passed=1 if status is CanonicalExecutionStatus.PASSED else 0,
        failed=1 if status is CanonicalExecutionStatus.FAILED else 0,
        skipped=0,
        errors=1 if status is CanonicalExecutionStatus.ERROR else 0,
        duration_seconds=0.1,
    )

    return CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        source_dirty=False,
        result=CanonicalExecutionResult(
            status=status,
            summary=summary,
            diagnostic=diagnostic,
        ),
        captured_at=datetime(
            2026,
            8,
            24,
            19,
            45,
            tzinfo=UTC,
        ),
    )


def test_gate_consumes_testing_evidence_for_pass(
    tmp_path: Path,
) -> None:
    execution = _EvidenceExecution(
        _evidence(CanonicalExecutionStatus.PASSED)
    )

    gate = PytestValidationGate(
        execution=execution,
        freshness_authority=_AlwaysFresh(),
        project_root=tmp_path,
    )

    result = gate.execute()

    assert execution.project_root == tmp_path
    assert execution.test_paths == ()
    assert result.status is ValidationStatus.PASSED


def test_gate_maps_failed_testing_evidence_to_failed_gate(
    tmp_path: Path,
) -> None:
    gate = PytestValidationGate(
        execution=_EvidenceExecution(
            _evidence(
                CanonicalExecutionStatus.FAILED,
                diagnostic="pytest failure",
            )
        ),
        freshness_authority=_AlwaysFresh(),
        project_root=tmp_path,
    )

    result = gate.execute()

    assert result.status is ValidationStatus.FAILED
    assert result.diagnostic == "pytest failure"


def test_gate_maps_error_testing_evidence_to_error_gate(
    tmp_path: Path,
) -> None:
    gate = PytestValidationGate(
        execution=_EvidenceExecution(
            _evidence(
                CanonicalExecutionStatus.ERROR,
                diagnostic="pytest execution error",
            )
        ),
        freshness_authority=_AlwaysFresh(),
        project_root=tmp_path,
    )

    result = gate.execute()

    assert result.status is ValidationStatus.ERROR
    assert result.diagnostic == "pytest execution error"


def test_gate_preserves_native_pytest_exit_code(
    tmp_path: Path,
) -> None:
    """Preserve runner-native exit semantics through Testing Evidence."""

    evidence = CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        source_dirty=False,
        result=CanonicalExecutionResult(
            status=CanonicalExecutionStatus.ERROR,
            summary=CanonicalExecutionSummary(
                discovered=0,
                executed=0,
                passed=0,
                failed=0,
                skipped=0,
                errors=0,
                duration_seconds=0.1,
            ),
            diagnostic="no tests collected",
        ),
        captured_at=datetime(
            2026,
            8,
            24,
            19,
            45,
            tzinfo=UTC,
        ),
        native_exit_code=5,
    )

    result = PytestValidationGate(
        execution=_EvidenceExecution(evidence),
        freshness_authority=_AlwaysFresh(),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.exit_code == 5
    assert result.diagnostic == "no tests collected"


def test_gate_result_retains_exact_testing_evidence(
    tmp_path: Path,
) -> None:
    evidence = _evidence(
        CanonicalExecutionStatus.PASSED,
    )

    result = PytestValidationGate(
        execution=_EvidenceExecution(evidence),
        freshness_authority=_AlwaysFresh(),
        project_root=tmp_path,
    ).execute()

    assert result.testing_evidence is evidence
    assert result.testing_evidence.execution_id is evidence.execution_id
    assert result.testing_evidence.source_revision == evidence.source_revision
    assert result.testing_evidence.captured_at == evidence.captured_at
