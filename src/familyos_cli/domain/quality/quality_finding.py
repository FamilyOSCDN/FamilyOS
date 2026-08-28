from dataclasses import dataclass

from familyos_cli.domain.quality.quality_domain import QualityDomain
from familyos_cli.domain.quality.quality_finding_id import QualityFindingId
from familyos_cli.domain.quality.quality_rule_id import QualityRuleId
from familyos_cli.domain.quality.quality_severity import QualitySeverity
from familyos_cli.domain.quality.quality_status import QualityStatus
from familyos_cli.domain.quality.quality_target import QualityTarget


@dataclass(frozen=True, slots=True)
class QualityFinding:
    id: QualityFindingId
    rule_id: QualityRuleId
    domain: QualityDomain
    severity: QualitySeverity
    status: QualityStatus
    message: str
    target: QualityTarget
    location: str | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for v, t, n in (
            (self.id, QualityFindingId, "id"),
            (self.rule_id, QualityRuleId, "rule_id"),
            (self.domain, QualityDomain, "domain"),
            (self.severity, QualitySeverity, "severity"),
            (self.status, QualityStatus, "status"),
            (self.target, QualityTarget, "target"),
        ):
            if not isinstance(v, t):
                raise TypeError(f"QualityFinding {n} must be a {t.__name__}")
        if not isinstance(self.message, str):
            raise TypeError("QualityFinding message must be a str")
        if not self.message:
            raise ValueError("QualityFinding message must be non-empty")
        if self.location is not None:
            if not isinstance(self.location, str):
                raise TypeError("QualityFinding location must be a str")
            if not self.location:
                raise ValueError("QualityFinding location must be non-empty")
        if not isinstance(self.evidence_ids, tuple):
            raise TypeError("QualityFinding evidence_ids must be a tuple")
        for e in self.evidence_ids:
            if not isinstance(e, str):
                raise TypeError("QualityFinding evidence_ids must contain str values")
            if not e.startswith("QLT-EVID-"):
                raise ValueError(
                    "QualityFinding evidence_ids must use the QLT-EVID- namespace"
                )
            s = e.removeprefix("QLT-EVID-")
            if not s:
                raise ValueError(
                    "QualityFinding evidence_ids must contain a non-empty suffix"
                )
            if e != e.strip() or any(c.isspace() for c in s):
                raise ValueError(
                    "QualityFinding evidence_ids must be canonical identifiers"
                )
