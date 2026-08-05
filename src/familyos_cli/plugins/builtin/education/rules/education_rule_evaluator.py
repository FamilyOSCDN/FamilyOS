"""Education rule evaluator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.rules.education_rule import (
    EducationRule,
)


class EducationRuleEvaluator:
    """Evaluate education rules."""

    def evaluate(
        self,
        rule: EducationRule,
        context: EducationContext,
    ) -> bool:
        """Evaluate rule against context."""

        if (
            context.required_level
            == EducationLevel.CRITICAL
        ):
            return rule.level == "critical"

        return True
