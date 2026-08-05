"""Tests for HealthPolicyEvaluator."""

from familyos_cli.plugins.builtin.health.domain.health_context import (
    HealthContext,
)
from familyos_cli.plugins.builtin.health.domain.health_decision import (
    HealthDecision,
)
from familyos_cli.plugins.builtin.health.domain.health_level import (
    HealthLevel,
)
from familyos_cli.plugins.builtin.health.policies.health_policy import (
    HealthPolicy,
)
from familyos_cli.plugins.builtin.health.policies.health_policy_evaluator import (
    HealthPolicyEvaluator,
)


def create_policy() -> HealthPolicy:
    """Create a test health policy."""

    return HealthPolicy(
        id="health.policy.basic",
        name="Basic Health Policy",
        version="1.0.0",
    )


def test_standard_health_level_allows_access() -> None:
    """Standard health levels should be allowed."""

    evaluator = HealthPolicyEvaluator()

    context = HealthContext(
        domain_name="family",
        subject="member",
        required_level=HealthLevel.STANDARD,
    )

    decision = evaluator.evaluate(
        create_policy(),
        context,
    )

    assert decision == HealthDecision.ALLOW


def test_critical_health_level_requires_review() -> None:
    """Critical health levels require review."""

    evaluator = HealthPolicyEvaluator()

    context = HealthContext(
        domain_name="family",
        subject="member",
        required_level=HealthLevel.CRITICAL,
    )

    decision = evaluator.evaluate(
        create_policy(),
        context,
    )

    assert decision == HealthDecision.REVIEW
