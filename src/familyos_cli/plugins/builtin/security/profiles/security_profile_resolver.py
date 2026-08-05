"""Security profile resolver."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)
from familyos_cli.plugins.builtin.security.profiles.security_profile import (
    SecurityProfile,
)


class SecurityProfileResolver:
    """Resolve security profiles."""

    def resolve_level(
        self,
        profile: SecurityProfile,
    ) -> SecurityLevel:
        """Resolve the security level of a profile."""

        return SecurityLevel(
            profile.level.lower(),
        )
