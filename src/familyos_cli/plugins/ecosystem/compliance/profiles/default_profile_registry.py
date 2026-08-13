"""Default compliance profile registry factory."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.profile_registry import (
    ProfileRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.profiles.official_profile import (
    OFFICIAL_PROFILE,
)


def build_default_profile_registry() -> ProfileRegistry:
    """Build the default compliance profile registry."""

    registry = ProfileRegistry()

    registry.register(OFFICIAL_PROFILE)

    return registry
