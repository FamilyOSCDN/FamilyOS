"""Governed construction boundary for version-controlled Quality profiles."""

from dataclasses import dataclass

from familyos_cli.domain.quality import QualityCheckId, QualityProfile


@dataclass(frozen=True, slots=True)
class QualityProfileDefinition:
    """Validate one governed profile against an explicit known-check set."""

    profile: QualityProfile
    known_check_ids: tuple[QualityCheckId, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.profile, QualityProfile):
            raise TypeError("profile must be a QualityProfile")
        if not isinstance(self.known_check_ids, tuple) or not all(
            isinstance(value, QualityCheckId) for value in self.known_check_ids
        ):
            raise TypeError("known_check_ids must contain QualityCheckId values")
        if len(set(self.known_check_ids)) != len(self.known_check_ids):
            raise ValueError("known_check_ids must not contain duplicates")

        known = set(self.known_check_ids)
        unknown = tuple(
            check_id for check_id in self.profile.required_checks if check_id not in known
        )
        if unknown:
            values = ", ".join(str(check_id) for check_id in unknown)
            raise ValueError(
                f"Quality profile '{self.profile.reference}' contains "
                f"unknown required checks: {values}"
            )
