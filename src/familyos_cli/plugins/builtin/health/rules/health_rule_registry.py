"""Health rule registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.rules.health_rule import (
    HealthRule,
)


class HealthRuleRegistry:
    """Registry for FamilyOS health rules."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._rules: dict[str, HealthRule] = {}

    def register(
        self,
        rule: HealthRule,
    ) -> None:
        """Register a health rule."""

        self._rules[rule.id] = rule

    def get(
        self,
        rule_id: str,
    ) -> HealthRule | None:
        """Return a rule by identifier."""

        return self._rules.get(
            rule_id,
        )

    def list(
        self,
    ) -> tuple[HealthRule, ...]:
        """Return registered rules."""

        return tuple(
            self._rules.values(),
        )
