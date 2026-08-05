"""Education validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.validation.education_validation_result import (
    EducationValidationResult,
)


class EducationValidator:
    """Validate education contexts."""

    def validate(
        self,
        context: EducationContext,
    ) -> EducationValidationResult:
        """Validate education context."""

        if (
            context.required_level
            == EducationLevel.CRITICAL
        ):
            return EducationValidationResult(
                valid=False,
                message=(
                    "Critical education review required."
                ),
            )

        return EducationValidationResult(
            valid=True,
            message=(
                "Education context validated."
            ),
        )
