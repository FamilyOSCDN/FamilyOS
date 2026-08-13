"""Security profile registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.profiles.security_profile import (
    SecurityProfile,
)


class SecurityProfileRegistry:
    """Registry for FamilyOS security profiles."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._profiles: dict[str, SecurityProfile] = {}

    def register(
        self,
        profile: SecurityProfile,
    ) -> None:
        """Register a security profile."""

        if profile.id in self._profiles:
            raise ValueError(
                f"Security profile '{profile.id}' already registered.",
            )

        self._profiles[
            profile.id
        ] = profile

    def get(
        self,
        profile_id: str,
    ) -> SecurityProfile | None:
        """Return a profile by identifier."""

        return self._profiles.get(
            profile_id,
        )

    def list(
        self,
    ) -> tuple[SecurityProfile, ...]:
        """Return registered profiles."""

        return tuple(
            self._profiles.values(),
        )
