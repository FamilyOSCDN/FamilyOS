"""Stable identity for a canonical Quality check."""

from dataclasses import dataclass

from familyos_cli.domain.quality._identifier import validate_quality_identifier


@dataclass(frozen=True, slots=True)
class QualityCheckId:
    """Stable Quality check identity in the QLT-CHECK namespace."""

    value: str

    def __post_init__(self) -> None:
        validate_quality_identifier(
            self.value,
            namespace="QLT-CHECK",
            type_name="QualityCheckId",
        )

    def __str__(self) -> str:
        return self.value
