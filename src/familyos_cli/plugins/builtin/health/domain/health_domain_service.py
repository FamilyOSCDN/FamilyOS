"""Health domain service."""

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


class HealthDomainService:
    """Evaluate health domain contexts."""

    def evaluate(
        self,
        context: HealthContext,
    ) -> HealthDecision:
        """Evaluate a health context."""

        if context.required_level == HealthLevel.CRITICAL:
            return HealthDecision.REVIEW

        return HealthDecision.ALLOW
