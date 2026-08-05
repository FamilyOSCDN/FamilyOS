"""Education policy evaluator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.policies.education_policy import (
    EducationPolicy,
)


class EducationPolicyEvaluator:
    """Evaluate education policies."""

    def evaluate(
        self,
        policy: EducationPolicy,
        context: EducationContext,
    ) -> bool:
        """Evaluate a policy against a context."""

        if (
            context.required_level
            == EducationLevel.CRITICAL
        ):
            return policy.level == "critical"

        return True
