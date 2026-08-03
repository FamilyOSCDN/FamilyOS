import pytest

from familyos_cli.plugins.builtin.health.profiles.health_profile import (
    HealthProfile,
)
from familyos_cli.plugins.builtin.health.profiles.health_profile_registry import (
    HealthProfileRegistry,
)


def create_profile() -> HealthProfile:
    return HealthProfile(
        id="health-001",
        person_id="person-001",
    )


def test_registry_registers_profile() -> None:
    registry = HealthProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.contains(
        "health-001",
    )


def test_registry_returns_profile() -> None:
    registry = HealthProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    assert registry.get(
        "health-001",
    ) == profile


def test_registry_rejects_duplicate_profile() -> None:
    registry = HealthProfileRegistry()

    profile = create_profile()

    registry.register(
        profile,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            profile,
        )
