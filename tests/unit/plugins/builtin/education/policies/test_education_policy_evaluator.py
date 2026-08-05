"""Tests for EducationPolicyEvaluator."""

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.policies.education_policy import (
    EducationPolicy,
)
from familyos_cli.plugins.builtin.education.policies.education_policy_evaluator import (
    EducationPolicyEvaluator,
)


def test_standard_context_accepts_policy() -> None:
    """Standard context accepts policy."""

    evaluator = EducationPolicyEvaluator()

    policy = EducationPolicy(
        id="education.policy.standard",
        name="Standard Policy",
        level="standard",
    )

    context = EducationContext(
        domain_name="learning",
        subject="student",
        required_level=EducationLevel.STANDARD,
    )

    assert evaluator.evaluate(
        policy,
        context,
    ) is True


def test_critical_context_requires_critical_policy() -> None:
    """Critical context checks policy level."""

    evaluator = EducationPolicyEvaluator()

    policy = EducationPolicy(
        id="education.policy.standard",
        name="Standard Policy",
        level="standard",
    )

    context = EducationContext(
        domain_name="learning",
        subject="student",
        required_level=EducationLevel.CRITICAL,
    )

    assert evaluator.evaluate(
        policy,
        context,
    ) is False
