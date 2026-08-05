"""Tests for SecurityPolicyEvaluator."""

from familyos_cli.plugins.builtin.security.domain.security_context import (
    SecurityContext,
)
from familyos_cli.plugins.builtin.security.domain.security_decision import (
    SecurityDecision,
)
from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)
from familyos_cli.plugins.builtin.security.policies.security_policy import (
    SecurityPolicy,
)
from familyos_cli.plugins.builtin.security.policies.security_policy_evaluator import (
    SecurityPolicyEvaluator,
)


def create_policy() -> SecurityPolicy:
    """Create a test security policy."""

    return SecurityPolicy(
        id="security.policy.default",
        name="Default Security Policy",
        version="1.0.0",
        description="Default security requirements.",
    )


def test_high_security_level_allows_access() -> None:
    """High security level should be allowed."""

    evaluator = SecurityPolicyEvaluator()

    context = SecurityContext(
        domain_name="family",
        resource="profile",
        required_level=SecurityLevel.HIGH,
    )

    decision = evaluator.evaluate(
        create_policy(),
        context,
    )

    assert decision == SecurityDecision.ALLOW


def test_critical_security_level_requires_review() -> None:
    """Critical security level should require review."""

    evaluator = SecurityPolicyEvaluator()

    context = SecurityContext(
        domain_name="family",
        resource="identity",
        required_level=SecurityLevel.CRITICAL,
    )

    decision = evaluator.evaluate(
        create_policy(),
        context,
    )

    assert decision == SecurityDecision.REVIEW
