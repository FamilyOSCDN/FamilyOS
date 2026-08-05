"""Tests for EducationRuleEvaluator."""

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.rules.education_rule import (
    EducationRule,
)
from familyos_cli.plugins.builtin.education.rules.education_rule_evaluator import (
    EducationRuleEvaluator,
)


def test_standard_context_accepts_rule() -> None:
    """Standard context accepts rule."""

    evaluator = EducationRuleEvaluator()

    rule = EducationRule(
        id="education.rule.standard",
        name="Standard Rule",
        level="standard",
    )

    context = EducationContext(
        domain_name="learning",
        subject="student",
        required_level=EducationLevel.STANDARD,
    )

    assert evaluator.evaluate(
        rule,
        context,
    ) is True


def test_critical_context_requires_critical_rule() -> None:
    """Critical context checks rule level."""

    evaluator = EducationRuleEvaluator()

    rule = EducationRule(
        id="education.rule.standard",
        name="Standard Rule",
        level="standard",
    )

    context = EducationContext(
        domain_name="learning",
        subject="student",
        required_level=EducationLevel.CRITICAL,
    )

    assert evaluator.evaluate(
        rule,
        context,
    ) is False
