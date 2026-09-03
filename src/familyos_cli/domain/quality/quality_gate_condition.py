from dataclasses import dataclass

from familyos_cli.domain.quality.quality_check_id import QualityCheckId
from familyos_cli.domain.quality.quality_evidence_id import QualityEvidenceId
from familyos_cli.domain.quality.quality_finding_id import QualityFindingId
from familyos_cli.domain.quality.quality_rule_id import QualityRuleId


@dataclass(frozen=True, slots=True)
class QualityGateCondition:
    code: str
    message: str
    check_id: QualityCheckId | None = None
    finding_ids: tuple[QualityFindingId, ...] = ()
    rule_ids: tuple[QualityRuleId, ...] = ()
    evidence_ids: tuple[QualityEvidenceId, ...] = ()

    def __post_init__(self) -> None:
        for name in ("code", "message"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Gate condition {name} must be a non-empty string")
        if self.check_id is not None and not isinstance(self.check_id, QualityCheckId):
            raise TypeError("Gate condition check_id must be a QualityCheckId or None")
        for name, kind in (
            ("finding_ids", QualityFindingId),
            ("rule_ids", QualityRuleId),
            ("evidence_ids", QualityEvidenceId),
        ):
            values = getattr(self, name)
            if not isinstance(values, tuple) or not all(
                isinstance(value, kind) for value in values
            ):
                raise TypeError(
                    f"Gate condition {name} must contain canonical identifiers"
                )
            if len(set(values)) != len(values):
                raise ValueError(f"Gate condition {name} must be unique")
