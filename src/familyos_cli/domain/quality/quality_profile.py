from dataclasses import dataclass

from familyos_cli.domain.quality.quality_check_id import QualityCheckId
from familyos_cli.domain.quality.quality_domain import QualityDomain
from familyos_cli.domain.quality.quality_profile_id import QualityProfileId
from familyos_cli.domain.quality.quality_severity import QualitySeverity


def _non_empty_string(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"QualityProfile {name} must be a str")
    if not value:
        raise ValueError(f"QualityProfile {name} must be non-empty")


@dataclass(frozen=True, slots=True)
class QualityProfile:
    id: QualityProfileId
    version: str
    target_types: tuple[str, ...]
    required_checks: tuple[QualityCheckId, ...]
    required_domains: tuple[QualityDomain, ...]
    severity_policy: tuple[tuple[QualitySeverity, bool], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.id, QualityProfileId):
            raise TypeError("QualityProfile id must be a QualityProfileId")
        _non_empty_string(self.version, "version")

        if not isinstance(self.target_types, tuple):
            raise TypeError("QualityProfile target_types must be a tuple")
        for target_type in self.target_types:
            _non_empty_string(target_type, "target_types entries")
        if len(set(self.target_types)) != len(self.target_types):
            raise ValueError("QualityProfile target_types must not contain duplicates")

        if not isinstance(self.required_checks, tuple) or not all(
            isinstance(value, QualityCheckId) for value in self.required_checks
        ):
            raise TypeError(
                "QualityProfile required_checks must contain QualityCheckId values"
            )
        if len(set(self.required_checks)) != len(self.required_checks):
            raise ValueError("QualityProfile required_checks must not contain duplicates")

        if not isinstance(self.required_domains, tuple) or not all(
            isinstance(value, QualityDomain) for value in self.required_domains
        ):
            raise TypeError(
                "QualityProfile required_domains must contain QualityDomain values"
            )
        if len(set(self.required_domains)) != len(self.required_domains):
            raise ValueError("QualityProfile required_domains must not contain duplicates")

        if not isinstance(self.severity_policy, tuple):
            raise TypeError("QualityProfile severity_policy must be a tuple")
        severities: list[QualitySeverity] = []
        for entry in self.severity_policy:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise TypeError(
                    "QualityProfile severity_policy entries must be "
                    "(QualitySeverity, bool) tuples"
                )
            severity, blocking = entry
            if not isinstance(severity, QualitySeverity):
                raise TypeError(
                    "QualityProfile severity_policy severity must be a QualitySeverity"
                )
            if not isinstance(blocking, bool):
                raise TypeError(
                    "QualityProfile severity_policy blocking value must be a bool"
                )
            severities.append(severity)
        if len(set(severities)) != len(severities):
            raise ValueError(
                "QualityProfile severity_policy must not contain duplicate severities"
            )

    def applies_to(self, target_type: str) -> bool:
        _non_empty_string(target_type, "target_type")
        return target_type in self.target_types

    @property
    def reference(self) -> str:
        return f"{self.id}@{self.version}"

    def to_dict(self) -> dict[str, object]:
        return {
            "id": str(self.id),
            "version": self.version,
            "target_types": list(self.target_types),
            "required_checks": [str(value) for value in self.required_checks],
            "required_domains": [str(value) for value in self.required_domains],
            "severity_policy": [
                {"severity": severity.value, "blocking": blocking}
                for severity, blocking in self.severity_policy
            ],
        }
