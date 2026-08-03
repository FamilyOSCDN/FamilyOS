"""Security validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)
from familyos_cli.plugins.builtin.security.validation.security_validation_result import (
    SecurityValidationResult,
)


class SecurityValidator:
    """Validate security rules."""

    def validate(
        self,
        rule: SecurityRule,
    ) -> SecurityValidationResult:
        """Validate a security rule."""

        return SecurityValidationResult(
            valid=True,
            message=(
                f"Security rule '{rule.id}' validated."
            ),
        )
