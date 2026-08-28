from dataclasses import dataclass

from familyos_cli.domain.quality._identifier import validate_quality_identifier


@dataclass(frozen=True, slots=True)
class QualityDomain:
    value: str

    def __post_init__(self) -> None:
        validate_quality_identifier(
            self.value, namespace="QLT-DOM", type_name="QualityDomain"
        )

    def __str__(self) -> str:
        return self.value


INITIAL_QUALITY_DOMAINS = tuple(
    QualityDomain(v)
    for v in (
        "QLT-DOM-COR",
        "QLT-DOM-ARC",
        "QLT-DOM-MNT",
        "QLT-DOM-REL",
        "QLT-DOM-SEC",
        "QLT-DOM-PER",
        "QLT-DOM-TST",
        "QLT-DOM-DOC",
        "QLT-DOM-CMP",
        "QLT-DOM-DEP",
        "QLT-DOM-CPL",
        "QLT-DOM-OBS",
        "QLT-DOM-BLD",
        "QLT-DOM-RLS",
        "QLT-DOM-INF",
        "QLT-DOM-DXE",
        "QLT-DOM-GOV",
    )
)
