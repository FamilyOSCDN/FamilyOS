"""Security domain service."""

from __future__ import annotations

from .security_context import SecurityContext
from .security_decision import SecurityDecision
from .security_level import SecurityLevel


class SecurityDomainService:
    """Domain service responsible for security decisions."""

    def evaluate(
        self,
        context: SecurityContext,
    ) -> SecurityDecision:
        """Evaluate a security context."""

        if context.required_level == SecurityLevel.CRITICAL:
            return SecurityDecision.REVIEW

        return SecurityDecision.ALLOW
