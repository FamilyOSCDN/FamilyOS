"""Security policy evaluator."""

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
from familyos_cli.plugins.builtin.security.policies.security_policy import (
    SecurityPolicy,
)


class SecurityPolicyEvaluator:
    """Evaluate security policies."""

    def evaluate(
        self,
        policy: SecurityPolicy,
        context: SecurityContext,
    ) -> SecurityDecision:
        """Evaluate a security policy."""

        if context.required_level == SecurityLevel.CRITICAL:
            return SecurityDecision.REVIEW

        return SecurityDecision.ALLOW
