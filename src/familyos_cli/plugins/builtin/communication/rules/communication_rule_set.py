"""Communication rule collection."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.communication.rules.communication_rule import (
    CommunicationRule,
)


@dataclass(frozen=True, slots=True)
class CommunicationRuleSet:
    """Collection of communication rules."""

    rules: tuple[
        CommunicationRule,
        ...,
    ] = ()

    def __post_init__(self) -> None:
        """Validate uniqueness."""

        ids = [
            rule.id
            for rule in self.rules
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Communication rule identifiers must be unique."
            )

    def list(
        self,
    ) -> tuple[
        CommunicationRule,
        ...,
    ]:
        """Return all rules."""

        return self.rules

    def get(
        self,
        rule_id: str,
    ) -> CommunicationRule | None:
        """Return one rule."""

        for rule in self.rules:
            if rule.id == rule_id:
                return rule

        return None
