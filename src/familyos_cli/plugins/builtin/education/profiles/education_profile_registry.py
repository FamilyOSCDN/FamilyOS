"""Education profile registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.profiles.education_profile import (
    EducationProfile,
)


class EducationProfileRegistry:
    """Store education profiles."""

    def __init__(self) -> None:
        self._profiles: dict[str, EducationProfile] = {}

    def register(
        self,
        profile: EducationProfile,
    ) -> None:
        """Register a profile."""

        self._profiles[profile.id] = profile

    def get(
        self,
        profile_id: str,
    ) -> EducationProfile | None:
        """Get profile by identifier."""

        return self._profiles.get(
            profile_id,
        )

    def list(
        self,
    ) -> tuple[EducationProfile, ...]:
        """List profiles."""

        return tuple(
            self._profiles.values(),
        )
