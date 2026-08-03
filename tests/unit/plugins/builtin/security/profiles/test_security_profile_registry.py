from familyos_cli.plugins.builtin.security.profiles.security_profile import (
    SecurityProfile,
)
from familyos_cli.plugins.builtin.security.profiles.security_profile_registry import (
    SecurityProfileRegistry,
)


def create_profile(
    profile_id: str = "security.profile.basic",
) -> SecurityProfile:
    """Create a test security profile."""

    return SecurityProfile(
        id=profile_id,
        name="Basic Security Profile",
        version="1.0.0",
        level="BASIC",
        description="Basic security profile.",
    )


def test_registry_registers_profile() -> None:
    registry = SecurityProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.get(
        profile.id,
    ) == profile


def test_registry_returns_none_for_unknown_profile() -> None:
    registry = SecurityProfileRegistry()

    assert registry.get(
        "security.profile.unknown",
    ) is None


def test_registry_lists_registered_profiles() -> None:
    registry = SecurityProfileRegistry()

    first = create_profile(
        "security.profile.first",
    )
    second = create_profile(
        "security.profile.second",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    profiles = registry.list()

    assert profiles == (
        first,
        second,
    )


def test_registry_replaces_profile_with_same_identifier() -> None:
    registry = SecurityProfileRegistry()

    first = create_profile()

    second = SecurityProfile(
        id="security.profile.basic",
        name="Updated Security Profile",
        version="2.0.0",
        level="ADVANCED",
        description="Updated security profile.",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.get(
        "security.profile.basic",
    ) == second
