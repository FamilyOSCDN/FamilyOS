from dataclasses import dataclass
from datetime import datetime

from familyos_cli.domain.quality.quality_evidence_id import QualityEvidenceId
from familyos_cli.domain.quality.quality_evidence_result import QualityEvidenceResult
from familyos_cli.domain.quality.quality_evidence_type import QualityEvidenceType
from familyos_cli.domain.quality.quality_requirement_id import QualityRequirementId
from familyos_cli.domain.quality.quality_rule_id import QualityRuleId
from familyos_cli.domain.quality.quality_target import QualityTarget


def _required_text(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"QualityEvidence {name} must be a str")
    if not value:
        raise ValueError(f"QualityEvidence {name} must be non-empty")


@dataclass(frozen=True, slots=True)
class QualityEvidence:
    id: QualityEvidenceId
    type: QualityEvidenceType
    source: str
    target: QualityTarget
    result: QualityEvidenceResult
    created_at: datetime
    revision: str | None = None
    rule_id: QualityRuleId | None = None
    requirement_id: QualityRequirementId | None = None
    tool: str | None = None
    tool_version: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()
    artifact: str | None = None

    def __post_init__(self) -> None:
        for typed_value, expected_type, name in (
            (self.id, QualityEvidenceId, "id"),
            (self.type, QualityEvidenceType, "type"),
            (self.target, QualityTarget, "target"),
            (self.result, QualityEvidenceResult, "result"),
        ):
            if not isinstance(typed_value, expected_type):
                raise TypeError(
                    f"QualityEvidence {name} must be a {expected_type.__name__}"
                )

        _required_text(self.source, "source")

        if not isinstance(self.created_at, datetime):
            raise TypeError("QualityEvidence created_at must be a datetime")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("QualityEvidence created_at must be timezone-aware")

        for name in ("revision", "tool", "tool_version", "artifact"):
            value = getattr(self, name)
            if value is not None:
                _required_text(value, name)

        if self.rule_id is not None and not isinstance(
            self.rule_id,
            QualityRuleId,
        ):
            raise TypeError("QualityEvidence rule_id must be a QualityRuleId")

        if self.requirement_id is not None and not isinstance(
            self.requirement_id,
            QualityRequirementId,
        ):
            raise TypeError(
                "QualityEvidence requirement_id must be a QualityRequirementId"
            )

        if not isinstance(self.metadata, tuple):
            raise TypeError("QualityEvidence metadata must be a tuple")

        for entry in self.metadata:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise TypeError(
                    "QualityEvidence metadata entries must be (str, str) tuples"
                )
            key, metadata_value = entry
            if not isinstance(key, str) or not isinstance(metadata_value, str):
                raise TypeError(
                    "QualityEvidence metadata entries must contain str values"
                )
            if not key:
                raise ValueError("QualityEvidence metadata keys must be non-empty")
            if not metadata_value:
                raise ValueError("QualityEvidence metadata values must be non-empty")
