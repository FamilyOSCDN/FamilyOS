"""Tests for Testing Evidence freshness enforcement in pytest validation."""

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


class _Execution(TestingExecutionPort):
    def __init__(
        self,
        evidence: CanonicalTestingEvidence,
    ) -> None:
        self.evidence = evidence

    def execute(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> CanonicalTestingEvidence:
        return self.evidence


class _FreshnessAuthority(TestingEvidenceFreshnessPort):
    def __init__(
        self,
        freshness: CanonicalEvidenceFreshness,
    ) -> None:
        self.freshness = freshness
        self.project_root: Path | None = None
        self.evidence: CanonicalTestingEvidence | None = None

    def evaluate(
        self,
        *,
        project_root: Path,
        evidence: CanonicalTestingEvidence,
    ) -> CanonicalEvidenceFreshness:
        self.project_root = project_root
        self.evidence = evidence
        return self.freshness


def _evidence() -> CanonicalTestingEvidence:
    return CanonicalTestingEvidence(
        execution_id=CanonicalExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        source_dirty=False,
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
            15,
            tzinfo=UTC,
        ),
        native_exit_code=0,
    )


def test_fresh_evidence_can_satisfy_pytest_gate(
    tmp_path: Path,
) -> None:
    evidence = _evidence()
    freshness = _FreshnessAuthority(
        CanonicalEvidenceFreshness.FRESH
    )

    result = PytestValidationGate(
        execution=_Execution(evidence),
        freshness_authority=freshness,
        project_root=tmp_path,
    ).execute()

    assert freshness.project_root == tmp_path
    assert freshness.evidence is evidence
    assert result.status is ValidationStatus.PASSED


def test_stale_evidence_cannot_satisfy_pytest_gate(
    tmp_path: Path,
) -> None:
    result = PytestValidationGate(
        execution=_Execution(_evidence()),
        freshness_authority=_FreshnessAuthority(
            CanonicalEvidenceFreshness.STALE
        ),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.diagnostic == (
        "pytest testing evidence is stale for the current source state"
    )


def test_unknown_evidence_freshness_cannot_satisfy_pytest_gate(
    tmp_path: Path,
) -> None:
    result = PytestValidationGate(
        execution=_Execution(_evidence()),
        freshness_authority=_FreshnessAuthority(
            CanonicalEvidenceFreshness.UNKNOWN
        ),
        project_root=tmp_path,
    ).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.diagnostic == (
        "pytest testing evidence freshness cannot be established"
    )
