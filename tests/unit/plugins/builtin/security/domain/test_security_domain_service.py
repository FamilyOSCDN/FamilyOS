"""Tests for SecurityDomainService."""

from familyos_cli.plugins.builtin.security.domain.security_context import (
    SecurityContext,
)
from familyos_cli.plugins.builtin.security.domain.security_decision import (
    SecurityDecision,
)
from familyos_cli.plugins.builtin.security.domain.security_domain_service import (
    SecurityDomainService,
)
from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)


def test_standard_security_level_allows_access() -> None:
    """Standard security levels should allow access."""

    service = SecurityDomainService()

    context = SecurityContext(
        domain_name="family",
        resource="profile",
        required_level=SecurityLevel.HIGH,
    )

    assert service.evaluate(context) == SecurityDecision.ALLOW


def test_critical_security_level_requires_review() -> None:
    """Critical security levels require review."""

    service = SecurityDomainService()

    context = SecurityContext(
        domain_name="family",
        resource="identity",
        required_level=SecurityLevel.CRITICAL,
    )

    assert service.evaluate(context) == SecurityDecision.REVIEW
