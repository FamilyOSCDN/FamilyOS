"""Health profile registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.profiles.health_profile import (
    HealthProfile,
)


class HealthProfileRegistry:
    """Registry of health profiles."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._profiles: dict[str, HealthProfile] = {}

    def register(
        self,
        profile: HealthProfile,
    ) -> None:
        """Register health profile."""

        if profile.id in self._profiles:
            raise ValueError(
                f"Health profile '{profile.id}' already registered.",
            )

        self._profiles[
            profile.id
        ] = profile

    def get(
        self,
        profile_id: str,
    ) -> HealthProfile:
        """Return health profile."""

        try:
            return self._profiles[
                profile_id
            ]
        except KeyError as error:
            raise ValueError(
                f"Health profile '{profile_id}' not found.",
            ) from error

    def contains(
        self,
        profile_id: str,
    ) -> bool:
        """Return whether profile exists."""

        return profile_id in self._profiles

    def list(
        self,
    ) -> tuple[HealthProfile, ...]:
        """Return all profiles."""

        return tuple(
            self._profiles.values(),
        )

    def clear(
        self,
    ) -> None:
        """Clear registry."""

        self._profiles.clear()
