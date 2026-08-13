"""Education rule registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.rules.education_rule import (
    EducationRule,
)


class EducationRuleRegistry:
    """Store education rules."""

    def __init__(
        self,
    ) -> None:
        """Initialize an empty rule registry."""

        self._rules: dict[
            str,
            EducationRule,
        ] = {}

    def register(
        self,
        rule: EducationRule,
    ) -> None:
        """Register a rule with a unique identifier."""

        if rule.id in self._rules:
            raise ValueError(
                f"Education rule '{rule.id}' "
                "is already registered.",
            )

        self._rules[
            rule.id
        ] = rule

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
