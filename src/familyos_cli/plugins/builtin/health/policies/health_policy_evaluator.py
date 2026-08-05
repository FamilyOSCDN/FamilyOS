"""Health policy evaluator."""

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
from familyos_cli.plugins.builtin.health.policies.health_policy import (
    HealthPolicy,
)


class HealthPolicyEvaluator:
    """Evaluate health policies."""

    def evaluate(
        self,
        policy: HealthPolicy,
        context: HealthContext,
    ) -> HealthDecision:
        """Evaluate a health policy."""

        if context.required_level == HealthLevel.CRITICAL:
            return HealthDecision.REVIEW

        return HealthDecision.ALLOW
