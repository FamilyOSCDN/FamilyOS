from dataclasses import dataclass

from familyos_cli.domain.quality._identifier import validate_quality_identifier


@dataclass(frozen=True, slots=True)
class QualityRuleId:
    value: str

    def __post_init__(self) -> None:
        validate_quality_identifier(
            self.value, namespace="QLT-RULE", type_name="QualityRuleId"
        )

    def __str__(self) -> str:
        return self.value
