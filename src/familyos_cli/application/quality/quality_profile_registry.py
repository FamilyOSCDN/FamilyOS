"""Governed registry for canonical Quality Framework profiles."""
from familyos_cli.domain.quality import QualityProfile, QualityProfileId


class QualityProfileRegistry:
    """Own the explicit set of governed Quality Profiles."""

    def __init__(self) -> None:
        self._profiles: dict[tuple[QualityProfileId, str], QualityProfile] = {}

    def register(self, profile: QualityProfile) -> None:
        if not isinstance(profile, QualityProfile):
            raise TypeError("QualityProfileRegistry accepts QualityProfile values only")
        key = (profile.id, profile.version)
        if key in self._profiles:
            raise ValueError(f"Quality profile '{profile.reference}' is already registered")
        self._profiles[key] = profile

    def get(self, profile_id: QualityProfileId, version: str) -> QualityProfile:
        if not isinstance(profile_id, QualityProfileId):
            raise TypeError("profile_id must be a QualityProfileId")
        if not isinstance(version, str):
            raise TypeError("version must be a str")
        if not version:
            raise ValueError("version must be non-empty")
        try:
            return self._profiles[(profile_id, version)]
        except KeyError as error:
            raise ValueError(
                f"Quality profile '{profile_id}@{version}' is not registered"
            ) from error

    def list(self) -> tuple[QualityProfile, ...]:
        return tuple(
            self._profiles[key]
            for key in sorted(self._profiles, key=lambda value: (str(value[0]), value[1]))
        )
