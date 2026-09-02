from dataclasses import dataclass

from familyos_cli.domain.quality._identifier import validate_quality_identifier


@dataclass(frozen=True, slots=True)
class QualityProfileId:
    value: str

    def __post_init__(self) -> None:
        validate_quality_identifier(
            self.value, namespace="QLT-PROFILE", type_name="QualityProfileId"
        )

    def __str__(self) -> str:
        return self.value
