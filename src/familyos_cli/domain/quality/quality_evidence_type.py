import re
from dataclasses import dataclass

_EVIDENCE_TYPE_PATTERN = re.compile(r"^[A-Z0-9_]+$")


@dataclass(frozen=True, slots=True)
class QualityEvidenceType:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("QualityEvidenceType value must be a str")
        if not self.value:
            raise ValueError("QualityEvidenceType value must be non-empty")
        if self.value != self.value.strip() or any(
            character.isspace() for character in self.value
        ):
            raise ValueError("QualityEvidenceType value must be canonical")
        if _EVIDENCE_TYPE_PATTERN.fullmatch(self.value) is None:
            raise ValueError(
                "QualityEvidenceType value must contain only uppercase "
                "letters, digits, and underscores"
            )
        if self.value == "TYPE_CHECK":
            raise ValueError("TYPE_CHECK is not canonical; use TYPE_VERIFICATION")

    def __str__(self) -> str:
        return self.value


INITIAL_QUALITY_EVIDENCE_TYPES = tuple(
    QualityEvidenceType(value)
    for value in (
        "TEST",
        "STATIC_ANALYSIS",
        "TYPE_VERIFICATION",
        "ARCHITECTURE",
        "SECURITY",
        "DOCUMENTATION",
        "BUILD",
        "PERFORMANCE",
        "COMPATIBILITY",
        "COMPLIANCE",
        "OBSERVABILITY",
        "MANUAL_REVIEW",
        "METRIC",
    )
)
