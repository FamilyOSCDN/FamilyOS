"""Tests for the default compliance profile registry factory."""

from familyos_cli.plugins.ecosystem.compliance.profiles.default_profile_registry import (
    build_default_profile_registry,
)


def test_build_default_profile_registry_registers_official_profile() -> None:
    """The default registry includes the official profile."""

    registry = build_default_profile_registry()

    profile = registry.get("official")

    assert profile.id == "official"
