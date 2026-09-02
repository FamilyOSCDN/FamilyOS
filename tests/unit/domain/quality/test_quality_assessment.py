from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityEvidenceId,
    QualityFindingId,
    QualityStatus,
    QualityTarget,
)


def test_assessment_model() -> None:
    assessment = QualityAssessment(
        id=QualityAssessmentId("QLT-ASMT-001"),
        target=QualityTarget("repository", "familyos-cli", revision="abc123"),
        revision="abc123",
        profile="baseline",
        status=QualityStatus.PASS,
        quality_state=QualityAssessmentState.PASS,
        evidence_ids=(QualityEvidenceId("QLT-EVID-001"),),
        finding_ids=(QualityFindingId("QLT-FIND-001"),),
        created_at=datetime(2026, 9, 2, tzinfo=UTC),
    )
    assert str(assessment.id) == "QLT-ASMT-001"
    assert assessment.revision == "abc123"


def test_assessment_id_namespace() -> None:
    with pytest.raises(ValueError):
        QualityAssessmentId("QLT-CHECK-001")


def test_created_at_must_be_timezone_aware() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        QualityAssessment(
            id=QualityAssessmentId("QLT-ASMT-001"),
            target=QualityTarget("repository", "familyos-cli"),
            revision=None,
            profile="baseline",
            status=QualityStatus.UNKNOWN,
            quality_state=QualityAssessmentState.UNKNOWN,
            evidence_ids=(),
            finding_ids=(),
            created_at=datetime(2026, 9, 2),
        )


def test_assessment_revision_must_match_target_revision() -> None:
    with pytest.raises(ValueError, match="must match target revision"):
        QualityAssessment(
            id=QualityAssessmentId("QLT-ASMT-001"),
            target=QualityTarget("repository", "familyos-cli", revision="abc123"),
            revision="different",
            profile="baseline",
            status=QualityStatus.UNKNOWN,
            quality_state=QualityAssessmentState.UNKNOWN,
            evidence_ids=(),
            finding_ids=(),
            created_at=datetime(2026, 9, 2, tzinfo=UTC),
        )


def test_assessment_is_immutable() -> None:
    assessment = QualityAssessment(
        id=QualityAssessmentId("QLT-ASMT-001"),
        target=QualityTarget("repository", "familyos-cli", revision="abc123"),
        revision="abc123",
        profile="baseline",
        status=QualityStatus.PASS,
        quality_state=QualityAssessmentState.PASS,
        evidence_ids=(),
        finding_ids=(),
        created_at=datetime(2026, 9, 2, tzinfo=UTC),
    )

    with pytest.raises(FrozenInstanceError):
        assessment.profile = "other"  # type: ignore[misc]


def test_assessment_stable_serialization() -> None:
    assessment = QualityAssessment(
        id=QualityAssessmentId("QLT-ASMT-001"),
        target=QualityTarget(
            "repository",
            "familyos-cli",
            revision="abc123",
            version="1.0.0",
            path=".",
            metadata=(("language", "python"),),
        ),
        revision="abc123",
        profile="baseline",
        status=QualityStatus.WARNING,
        quality_state=QualityAssessmentState.PASS_WITH_WARNINGS,
        evidence_ids=(
            QualityEvidenceId("QLT-EVID-001"),
            QualityEvidenceId("QLT-EVID-002"),
        ),
        finding_ids=(QualityFindingId("QLT-FIND-001"),),
        created_at=datetime(2026, 9, 2, 9, 30, tzinfo=UTC),
    )

    assert assessment.to_dict() == {
        "id": "QLT-ASMT-001",
        "target": {
            "target_type": "repository",
            "identifier": "familyos-cli",
            "revision": "abc123",
            "version": "1.0.0",
            "path": ".",
            "metadata": [["language", "python"]],
        },
        "revision": "abc123",
        "profile": "baseline",
        "status": "WARNING",
        "quality_state": "PASS_WITH_WARNINGS",
        "evidence_ids": ["QLT-EVID-001", "QLT-EVID-002"],
        "finding_ids": ["QLT-FIND-001"],
        "created_at": "2026-09-02T09:30:00+00:00",
    }
