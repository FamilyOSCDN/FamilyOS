"""Tests for SecurityProfileResolver."""

from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)
from familyos_cli.plugins.builtin.security.profiles.security_profile import (
    SecurityProfile,
)
from familyos_cli.plugins.builtin.security.profiles.security_profile_resolver import (
    SecurityProfileResolver,
)


def test_resolver_returns_security_level() -> None:
    """Resolver converts profile level to SecurityLevel."""

    resolver = SecurityProfileResolver()

    profile = SecurityProfile(
        id="security.profile.critical",
        name="Critical Security Profile",
        version="1.0.0",
        level="critical",
    )

    level = resolver.resolve_level(
        profile,
    )

    assert level == SecurityLevel.CRITICAL
