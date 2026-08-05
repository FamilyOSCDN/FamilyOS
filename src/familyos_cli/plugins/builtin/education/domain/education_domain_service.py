"""Education domain service."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_decision import (
    EducationDecision,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)


class EducationDomainService:
    """Domain service for education decisions."""

    def evaluate(
        self,
        context: EducationContext,
    ) -> EducationDecision:
        """Evaluate education context."""

        if (
            context.required_level
            == EducationLevel.CRITICAL
        ):
            return EducationDecision.REVIEW

        return EducationDecision.ALLOW
