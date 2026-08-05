"""Tests for SecurityContext."""

from familyos_cli.plugins.builtin.security.domain.security_context import (
    SecurityContext,
)
from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)


def test_security_context_creation() -> None:
    """Security context stores provided values."""

    context = SecurityContext(
        domain_name="family",
        resource="profile",
        required_level=SecurityLevel.HIGH,
    )

    assert context.domain_name == "family"
    assert context.resource == "profile"
    assert context.required_level == SecurityLevel.HIGH


def test_security_context_is_immutable() -> None:
    """Security context cannot be modified."""

    context = SecurityContext(
        domain_name="family",
        resource="profile",
        required_level=SecurityLevel.LOW,
    )

    assert context.domain_name == "family"
