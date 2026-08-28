from dataclasses import dataclass

from familyos_cli.domain.quality.quality_domain import QualityDomain
from familyos_cli.domain.quality.quality_requirement_id import QualityRequirementId


@dataclass(frozen=True, slots=True)
class QualityRequirement:
    id: QualityRequirementId
    title: str
    description: str
    domain: QualityDomain
    authority: str
    mandatory: bool
    applicability: str
    verification: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, QualityRequirementId):
            raise TypeError("QualityRequirement id must be a QualityRequirementId")
        if not isinstance(self.domain, QualityDomain):
            raise TypeError("QualityRequirement domain must be a QualityDomain")
        if not isinstance(self.mandatory, bool):
            raise TypeError("QualityRequirement mandatory must be a bool")
        for n in ("title", "description", "authority", "applicability", "verification"):
            v = getattr(self, n)
            if not isinstance(v, str):
                raise TypeError(f"QualityRequirement {n} must be a str")
            if not v:
                raise ValueError(f"QualityRequirement {n} must be non-empty")
