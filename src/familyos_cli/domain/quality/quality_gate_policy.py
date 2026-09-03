from dataclasses import dataclass
from typing import Literal

from familyos_cli.domain.quality.quality_assessment_state import QualityAssessmentState
from familyos_cli.domain.quality.quality_gate_id import QualityGateId
from familyos_cli.domain.quality.quality_profile import QualityProfile
from familyos_cli.domain.quality.quality_status import QualityStatus


@dataclass(frozen=True, slots=True)
class QualityGatePolicy:
    gate_id: QualityGateId
    version: str
    authority: str
    profile: QualityProfile
    accepted_check_statuses: tuple[QualityStatus, ...]
    accepted_assessment_states: tuple[QualityAssessmentState, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.gate_id, QualityGateId):
            raise TypeError("gate_id must be a QualityGateId")
        for name in ("version", "authority"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Gate policy {name} must be a non-empty string")
        if not isinstance(self.profile, QualityProfile):
            raise TypeError("Gate policy profile must be a QualityProfile")
        if not self.profile.required_checks or not self.profile.target_types:
            raise ValueError(
                "Gate policy requires an applicable profile with required checks"
            )
        statuses = self.accepted_check_statuses
        if (
            not isinstance(statuses, tuple)
            or not statuses
            or not all(
                isinstance(value, QualityStatus)
                and value in (QualityStatus.PASS, QualityStatus.WARNING)
                for value in statuses
            )
            or len(set(statuses)) != len(statuses)
        ):
            raise ValueError(
                "Gate policy accepted check statuses must be unique positive statuses"
            )
        states = self.accepted_assessment_states
        if (
            not isinstance(states, tuple)
            or not states
            or not all(
                isinstance(value, QualityAssessmentState)
                and value
                in (
                    QualityAssessmentState.PASS,
                    QualityAssessmentState.PASS_WITH_WARNINGS,
                )
                for value in states
            )
            or len(set(states)) != len(states)
        ):
            raise ValueError(
                "Gate policy accepted assessment states must be unique positive states"
            )

    @property
    def reference(self) -> str:
        return f"{self.gate_id}@{self.version}"

    @property
    def mode(self) -> Literal["OBSERVE"]:
        return "OBSERVE"
