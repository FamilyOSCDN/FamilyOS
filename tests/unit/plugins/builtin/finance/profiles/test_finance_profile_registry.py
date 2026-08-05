"""Tests for FinanceProfileRegistry."""

from familyos_cli.plugins.builtin.finance.profiles.finance_profile import (
    FinanceProfile,
)
from familyos_cli.plugins.builtin.finance.profiles.finance_profile_registry import (
    FinanceProfileRegistry,
)


def create_profile(
    profile_id: str = "finance.profile.basic",
) -> FinanceProfile:
    """Create a test finance profile."""

    return FinanceProfile(
        id=profile_id,
        name="Basic Finance Profile",
        version="1.0.0",
        level="BASIC",
        description="Basic finance profile.",
    )


def test_registry_registers_profile() -> None:
    registry = FinanceProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.get(
        profile.id,
    ) == profile


def test_registry_returns_none_for_unknown_profile() -> None:
    registry = FinanceProfileRegistry()

    assert registry.get(
        "finance.profile.unknown",
    ) is None


def test_registry_lists_registered_profiles() -> None:
    registry = FinanceProfileRegistry()

    first = create_profile(
        "finance.profile.first",
    )
    second = create_profile(
        "finance.profile.second",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.list() == (
        first,
        second,
    )


def test_registry_replaces_profile_with_same_identifier() -> None:
    registry = FinanceProfileRegistry()

    first = create_profile()

    second = FinanceProfile(
        id="finance.profile.basic",
        name="Updated Finance Profile",
        version="2.0.0",
        level="STANDARD",
        description="Updated finance profile.",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.get(
        "finance.profile.basic",
    ) == second
