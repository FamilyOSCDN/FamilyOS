"""Security rule registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)


class SecurityRuleRegistry:
    """Registry for FamilyOS security rules."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._rules: dict[str, SecurityRule] = {}

    def register(
        self,
        rule: SecurityRule,
    ) -> None:
        """Register a security rule."""

        self._rules[rule.id] = rule

    def get(
        self,
        rule_id: str,
    ) -> SecurityRule | None:
        """Return a rule by identifier."""

        return self._rules.get(
            rule_id,
        )

    def list(
        self,
    ) -> tuple[SecurityRule, ...]:
        """Return registered rules."""

        return tuple(
            self._rules.values(),
        )
