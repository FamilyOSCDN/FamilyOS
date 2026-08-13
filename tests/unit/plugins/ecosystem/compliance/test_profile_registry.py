"""Tests for the compliance profile registry."""

import pytest

from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
)
from familyos_cli.plugins.ecosystem.compliance.profile_registry import (
    ProfileRegistry,
)


def _make_profile(profile_id: str = "test") -> ComplianceProfile:
    return ComplianceProfile(
        id=profile_id,
        version="1.0.0",
        description="Test profile.",
        included_rule_ids=(),
    )


def test_register_and_get_profile() -> None:
    """A registered profile can be retrieved by id."""

    registry = ProfileRegistry()
    profile = _make_profile()

    registry.register(profile)

    assert registry.get(profile.id) is profile


def test_register_duplicate_profile_raises() -> None:
    """Registering the same profile id twice raises ValueError."""

    registry = ProfileRegistry()
    registry.register(_make_profile())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(_make_profile())


def test_get_missing_profile_raises() -> None:
    """Retrieving an unregistered profile id raises ValueError."""

    registry = ProfileRegistry()

    with pytest.raises(ValueError, match="not registered"):
        registry.get("missing")


def test_list_returns_all_profiles() -> None:
    """list() returns every registered profile."""

    registry = ProfileRegistry()
    first = _make_profile("first")
    second = _make_profile("second")

    registry.register(first)
    registry.register(second)

    assert set(registry.list()) == {first, second}
