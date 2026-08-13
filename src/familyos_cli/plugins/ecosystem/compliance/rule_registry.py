"""Compliance rule registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)


@dataclass(slots=True)
class RuleRegistry:
    """Registry of governed compliance rules."""

    _rules: dict[str, ComplianceRule] = field(default_factory=dict)

    def register(
        self,
        rule: ComplianceRule,
    ) -> None:
        """Register a compliance rule by its stable identifier."""

        if rule.id in self._rules:
            raise ValueError(
                f"Compliance rule '{rule.id}' is already registered",
            )

        self._rules[rule.id] = rule

    def get(
        self,
        rule_id: str,
    ) -> ComplianceRule:
        """Retrieve a compliance rule by identifier."""

        if rule_id not in self._rules:
            raise ValueError(
                f"Compliance rule '{rule_id}' is not registered",
            )

        return self._rules[rule_id]

    def list(
        self,
    ) -> list[ComplianceRule]:
        """Return all registered compliance rules."""

        return list(self._rules.values())
