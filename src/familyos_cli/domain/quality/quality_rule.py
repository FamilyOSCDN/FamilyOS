from dataclasses import dataclass

from familyos_cli.domain.quality.quality_domain import QualityDomain
from familyos_cli.domain.quality.quality_requirement_id import QualityRequirementId
from familyos_cli.domain.quality.quality_rule_id import QualityRuleId
from familyos_cli.domain.quality.quality_severity import QualitySeverity


@dataclass(frozen=True, slots=True)
class QualityRule:
    id: QualityRuleId
    requirement_id: QualityRequirementId | None
    domain: QualityDomain
    severity: QualitySeverity
    description: str
    executor: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, QualityRuleId):
            raise TypeError("QualityRule id must be a QualityRuleId")
        if self.requirement_id is not None and not isinstance(
            self.requirement_id, QualityRequirementId
        ):
            raise TypeError("QualityRule requirement_id must be a QualityRequirementId")
        if not isinstance(self.domain, QualityDomain):
            raise TypeError("QualityRule domain must be a QualityDomain")
        if not isinstance(self.severity, QualitySeverity):
            raise TypeError("QualityRule severity must be a QualitySeverity")
        if not isinstance(self.description, str):
            raise TypeError("QualityRule description must be a str")
        if not self.description:
            raise ValueError("QualityRule description must be non-empty")
        if self.executor is not None:
            if not isinstance(self.executor, str):
                raise TypeError("QualityRule executor must be a str")
            if not self.executor:
                raise ValueError("QualityRule executor must be non-empty")
