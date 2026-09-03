"""Stable identity for a canonical Quality gate."""

from dataclasses import dataclass

from familyos_cli.domain.quality._identifier import validate_quality_identifier


@dataclass(frozen=True, slots=True)
class QualityGateId:
    """Stable Quality gate identity in the QLT-GATE namespace."""

    value: str

    def __post_init__(self) -> None:
        validate_quality_identifier(
            self.value,
            namespace="QLT-GATE",
            type_name="QualityGateId",
        )

    def __str__(self) -> str:
        return self.value
