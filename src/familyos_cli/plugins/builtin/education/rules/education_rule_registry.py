"""Education rule registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.rules.education_rule import (
    EducationRule,
)


class EducationRuleRegistry:
    """Store education rules."""

    def __init__(self) -> None:
        self._rules: dict[str, EducationRule] = {}

    def register(
        self,
        rule: EducationRule,
    ) -> None:
        """Register a rule."""

        self._rules[rule.id] = rule

    def get(
        self,
        rule_id: str,
    ) -> EducationRule | None:
        """Get rule by identifier."""

        return self._rules.get(
            rule_id,
        )

    def list(
        self,
    ) -> tuple[EducationRule, ...]:
        """List rules."""

        return tuple(
            self._rules.values(),
        )
