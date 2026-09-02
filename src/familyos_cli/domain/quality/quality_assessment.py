from dataclasses import dataclass
from datetime import datetime

from familyos_cli.domain.quality.quality_assessment_id import QualityAssessmentId
from familyos_cli.domain.quality.quality_assessment_state import QualityAssessmentState
from familyos_cli.domain.quality.quality_evidence_id import QualityEvidenceId
from familyos_cli.domain.quality.quality_finding_id import QualityFindingId
from familyos_cli.domain.quality.quality_status import QualityStatus
from familyos_cli.domain.quality.quality_target import QualityTarget


@dataclass(frozen=True, slots=True)
class QualityAssessment:
    id: QualityAssessmentId
    target: QualityTarget
    revision: str | None
    profile: str
    status: QualityStatus
    quality_state: QualityAssessmentState
    evidence_ids: tuple[QualityEvidenceId, ...]
    finding_ids: tuple[QualityFindingId, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.id, QualityAssessmentId):
            raise TypeError("QualityAssessment id must be a QualityAssessmentId")
        if not isinstance(self.target, QualityTarget):
            raise TypeError("QualityAssessment target must be a QualityTarget")
        if self.revision is not None and (
            not isinstance(self.revision, str) or not self.revision
        ):
            raise ValueError(
                "QualityAssessment revision must be a non-empty str or None"
            )
        if self.revision != self.target.revision:
            raise ValueError("QualityAssessment revision must match target revision")
        if not isinstance(self.profile, str):
            raise TypeError("QualityAssessment profile must be a str")
        if not self.profile:
            raise ValueError("QualityAssessment profile must be non-empty")
        if not isinstance(self.status, QualityStatus):
            raise TypeError("QualityAssessment status must be a QualityStatus")
        if not isinstance(self.quality_state, QualityAssessmentState):
            raise TypeError(
                "QualityAssessment quality_state must be a QualityAssessmentState"
            )
        if not isinstance(self.evidence_ids, tuple) or not all(
            isinstance(x, QualityEvidenceId) for x in self.evidence_ids
        ):
            raise TypeError(
                "QualityAssessment evidence_ids must contain QualityEvidenceId values"
            )
        if not isinstance(self.finding_ids, tuple) or not all(
            isinstance(x, QualityFindingId) for x in self.finding_ids
        ):
            raise TypeError(
                "QualityAssessment finding_ids must contain QualityFindingId values"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError("QualityAssessment created_at must be a datetime")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("QualityAssessment created_at must be timezone-aware")

    def to_dict(self) -> dict[str, object]:
        return {
            "id": str(self.id),
            "target": {
                "target_type": self.target.target_type,
                "identifier": self.target.identifier,
                "revision": self.target.revision,
                "version": self.target.version,
                "path": self.target.path,
                "metadata": [list(entry) for entry in self.target.metadata],
            },
            "revision": self.revision,
            "profile": self.profile,
            "status": self.status.value,
            "quality_state": self.quality_state.value,
            "evidence_ids": [str(value) for value in self.evidence_ids],
            "finding_ids": [str(value) for value in self.finding_ids],
            "created_at": self.created_at.isoformat(),
        }
