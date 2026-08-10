"""Tests for DocumentProfileResolver."""

from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)
from familyos_cli.plugins.builtin.documents.profiles.document_profile import (
    DocumentProfile,
)
from familyos_cli.plugins.builtin.documents.profiles.document_profile_resolver import (
    DocumentProfileResolver,
)


def test_resolver_returns_basic_level() -> None:
    """Resolver returns BASIC level."""

    resolver = DocumentProfileResolver()

    profile = DocumentProfile(
        id="documents.profile.basic",
        name="Basic Documents Profile",
        version="1.0.0",
        level="BASIC",
    )

    assert resolver.resolve(
        profile,
    ) == DocumentLevel.BASIC


def test_resolver_returns_critical_level() -> None:
    """Resolver returns CRITICAL level."""

    resolver = DocumentProfileResolver()

    profile = DocumentProfile(
        id="documents.profile.critical",
        name="Critical Documents Profile",
        version="1.0.0",
        level="CRITICAL",
    )

    assert resolver.resolve(
        profile,
    ) == DocumentLevel.CRITICAL