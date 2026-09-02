from dataclasses import dataclass

from familyos_cli.domain.quality._identifier import validate_quality_identifier


@dataclass(frozen=True, slots=True)
class QualityAssessmentId:
    value: str

    def __post_init__(self) -> None:
        validate_quality_identifier(
            self.value, namespace="QLT-ASMT", type_name="QualityAssessmentId"
        )

    def __str__(self) -> str:
        return self.value
