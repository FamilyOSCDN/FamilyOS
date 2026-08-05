"""Security rule evaluator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.domain.security_context import (
    SecurityContext,
)
from familyos_cli.plugins.builtin.security.domain.security_decision import (
    SecurityDecision,
)
from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)
from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)


class SecurityRuleEvaluator:
    """Evaluate security rules."""

    def evaluate(
        self,
        rule: SecurityRule,
        context: SecurityContext,
    ) -> SecurityDecision:
        """Evaluate a security rule."""

        if (
            rule.severity.lower() == "critical"
            or context.required_level == SecurityLevel.CRITICAL
        ):
            return SecurityDecision.REVIEW

        return SecurityDecision.ALLOW
