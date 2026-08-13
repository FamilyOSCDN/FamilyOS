"""Compliance profile registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
)


@dataclass(slots=True)
class ProfileRegistry:
    """Registry of governed compliance profiles."""

    _profiles: dict[str, ComplianceProfile] = field(default_factory=dict)

    def register(
        self,
        profile: ComplianceProfile,
    ) -> None:
        """Register a compliance profile by its stable identifier."""

        if profile.id in self._profiles:
            raise ValueError(
                f"Compliance profile '{profile.id}' is already registered",
            )

        self._profiles[profile.id] = profile

    def get(
        self,
        profile_id: str,
    ) -> ComplianceProfile:
        """Retrieve a compliance profile by identifier."""

        if profile_id not in self._profiles:
            raise ValueError(
                f"Compliance profile '{profile_id}' is not registered",
            )

        return self._profiles[profile_id]

    def list(
        self,
    ) -> list[ComplianceProfile]:
        """Return all registered compliance profiles."""

        return list(self._profiles.values())
