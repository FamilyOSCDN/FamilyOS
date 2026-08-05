"""Finance rule registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.rules.finance_rule import (
    FinanceRule,
)


class FinanceRuleRegistry:
    """Registry for FamilyOS finance rules."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._rules: dict[str, FinanceRule] = {}

    def register(
        self,
        rule: FinanceRule,
    ) -> None:
        """Register a finance rule."""

        self._rules[rule.id] = rule

    def get(
        self,
        rule_id: str,
    ) -> FinanceRule | None:
        """Return a rule by identifier."""

        return self._rules.get(
            rule_id,
        )

    def list(
        self,
    ) -> tuple[FinanceRule, ...]:
        """Return registered rules."""

        return tuple(
            self._rules.values(),
        )
