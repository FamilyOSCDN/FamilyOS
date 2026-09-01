"""Tests for the normalized Quality check result."""

from datetime import UTC, datetime

import pytest

from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)


def _target() -> QualityTarget:
    return QualityTarget(target_type="repository", identifier="familyos")


def _finding() -> QualityFinding:
    return QualityFinding(
        id=QualityFindingId("QLT-FIND-TEST-001"),
        rule_id=QualityRuleId("QLT-RULE-TEST-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.MEDIUM,
        status=QualityStatus.FAIL,
        message="quality violation",
        target=_target(),
    )


def _evidence() -> QualityEvidence:
    return QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-TEST-001"),
        type=QualityEvidenceType("TEST"),
        source="unit-test",
        target=_target(),
        result=QualityEvidenceResult.PASS,
        created_at=datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
    )


def test_pass_result_supports_zero_findings() -> None:
    result = QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-UNIT"),
        status=QualityStatus.PASS,
    )

    assert result.findings == ()
    assert result.evidence == ()
    assert result.duration_seconds == 0.0
    assert result.diagnostics == ()


def test_result_supports_multiple_findings_and_evidence() -> None:
    finding = _finding()
    evidence = _evidence()

    result = QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-UNIT"),
        status=QualityStatus.FAIL,
        findings=(finding, finding),
        evidence=(evidence,),
        duration_seconds=1.25,
        diagnostics=("one violation",),
    )

    assert result.findings == (finding, finding)
    assert result.evidence == (evidence,)
    assert result.duration_seconds == 1.25


@pytest.mark.parametrize("duration", (0, 0.0, 1, 1.5))
def test_result_accepts_non_negative_numeric_duration(
    duration: int | float,
) -> None:
    QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-UNIT"),
        status=QualityStatus.PASS,
        duration_seconds=duration,
    )


@pytest.mark.parametrize("duration", (-1, -0.1))
def test_result_rejects_negative_duration(duration: float) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        QualityCheckResult(
            check_id=QualityCheckId("QLT-CHECK-UNIT"),
            status=QualityStatus.ERROR,
            duration_seconds=duration,
        )


def test_result_rejects_boolean_duration() -> None:
    with pytest.raises(TypeError, match="numeric"):
        QualityCheckResult(
            check_id=QualityCheckId("QLT-CHECK-UNIT"),
            status=QualityStatus.PASS,
            duration_seconds=True,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("diagnostic", ("",))
def test_result_rejects_empty_diagnostic(diagnostic: str) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        QualityCheckResult(
            check_id=QualityCheckId("QLT-CHECK-UNIT"),
            status=QualityStatus.ERROR,
            diagnostics=(diagnostic,),
        )


def test_result_requires_tuple_collections() -> None:
    with pytest.raises(TypeError, match="findings must be a tuple"):
        QualityCheckResult(
            check_id=QualityCheckId("QLT-CHECK-UNIT"),
            status=QualityStatus.PASS,
            findings=[],  # type: ignore[arg-type]
        )


def test_result_is_immutable() -> None:
    result = QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-UNIT"),
        status=QualityStatus.PASS,
    )

    with pytest.raises(AttributeError):
        result.status = QualityStatus.FAIL  # type: ignore[misc]
