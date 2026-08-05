"""Finance profile registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.profiles.finance_profile import (
    FinanceProfile,
)


class FinanceProfileRegistry:
    """Registry for FamilyOS finance profiles."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._profiles: dict[str, FinanceProfile] = {}

    def register(
        self,
        profile: FinanceProfile,
    ) -> None:
        """Register a finance profile."""

        self._profiles[profile.id] = profile

    def get(
        self,
        profile_id: str,
    ) -> FinanceProfile | None:
        """Return a profile by identifier."""

        return self._profiles.get(
            profile_id,
        )

    def list(
        self,
    ) -> tuple[FinanceProfile, ...]:
        """Return registered profiles."""

        return tuple(
            self._profiles.values(),
        )
