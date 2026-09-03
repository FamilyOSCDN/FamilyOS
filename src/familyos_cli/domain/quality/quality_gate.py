from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from familyos_cli.domain.quality.gate_decision import GateDecision
from familyos_cli.domain.quality.quality_assessment_id import QualityAssessmentId
from familyos_cli.domain.quality.quality_gate_condition import QualityGateCondition
from familyos_cli.domain.quality.quality_gate_id import QualityGateId
from familyos_cli.domain.quality.quality_target import QualityTarget


@dataclass(frozen=True, slots=True)
class QualityGate:
    id: QualityGateId
    target: QualityTarget
    revision: str | None
    policy: str
    assessment_id: QualityAssessmentId | None
    decision: GateDecision
    blocking_conditions: tuple[QualityGateCondition, ...]
    evaluated_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.id, QualityGateId) or not isinstance(
            self.target, QualityTarget
        ):
            raise TypeError("Gate requires canonical identity and target")
        if self.revision != self.target.revision:
            raise ValueError("Gate revision must match target revision")
        if not isinstance(self.policy, str) or not self.policy.strip():
            raise ValueError("Gate policy reference must be non-empty")
        if self.assessment_id is not None and not isinstance(
            self.assessment_id, QualityAssessmentId
        ):
            raise TypeError("Gate assessment_id must be canonical or None")
        if not isinstance(self.decision, GateDecision):
            raise TypeError("Gate decision must be a GateDecision")
        if not isinstance(self.blocking_conditions, tuple) or not all(
            isinstance(value, QualityGateCondition)
            for value in self.blocking_conditions
        ):
            raise TypeError(
                "Gate blocking_conditions must contain QualityGateCondition values"
            )
        if self.decision is GateDecision.PASS and self.blocking_conditions:
            raise ValueError("PASS gate must not have blocking conditions")
        if self.decision is not GateDecision.PASS and not self.blocking_conditions:
            raise ValueError("Non-passing gate requires an explanation")
        if self.decision is not GateDecision.ERROR and (
            self.assessment_id is None or self.revision is None
        ):
            raise ValueError(
                "A reliable decision requires assessment identity and revision"
            )
        if not isinstance(self.evaluated_at, datetime):
            raise TypeError("Gate evaluated_at must be a datetime")
        if self.evaluated_at.tzinfo is None or self.evaluated_at.utcoffset() is None:
            raise ValueError("Gate evaluated_at must be timezone-aware")

    @property
    def mode(self) -> Literal["OBSERVE"]:
        return "OBSERVE"

    @property
    def prevents_progression(self) -> Literal[False]:
        return False
