"""Tests for FinanceProfileResolver."""

from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)
from familyos_cli.plugins.builtin.finance.profiles.finance_profile import (
    FinanceProfile,
)
from familyos_cli.plugins.builtin.finance.profiles.finance_profile_resolver import (
    FinanceProfileResolver,
)


def test_resolver_returns_basic_level() -> None:
    """Resolver returns BASIC level."""

    resolver = FinanceProfileResolver()

    profile = FinanceProfile(
        id="finance.profile.basic",
        name="Basic Finance Profile",
        version="1.0.0",
        level="BASIC",
    )

    assert resolver.resolve(
        profile,
    ) == FinanceLevel.BASIC


def test_resolver_returns_critical_level() -> None:
    """Resolver returns CRITICAL level."""

    resolver = FinanceProfileResolver()

    profile = FinanceProfile(
        id="finance.profile.critical",
        name="Critical Finance Profile",
        version="1.0.0",
        level="CRITICAL",
    )

    assert resolver.resolve(
        profile,
    ) == FinanceLevel.CRITICAL
