"""Health rule evaluator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.domain.health_context import (
    HealthContext,
)
from familyos_cli.plugins.builtin.health.domain.health_decision import (
    HealthDecision,
)
from familyos_cli.plugins.builtin.health.domain.health_level import (
    HealthLevel,
)
from familyos_cli.plugins.builtin.health.rules.health_rule import (
    HealthRule,
)


class HealthRuleEvaluator:
    """Evaluate health rules."""

    def evaluate(
        self,
        rule: HealthRule,
        context: HealthContext,
    ) -> HealthDecision:
        """Evaluate a health rule."""

        if (
            context.required_level
            == HealthLevel.CRITICAL
        ):
            return HealthDecision.REVIEW

        return HealthDecision.ALLOW
