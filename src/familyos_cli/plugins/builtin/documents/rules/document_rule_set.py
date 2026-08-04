"""Document rule set."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.documents.rules.document_rule import (
    DocumentRule,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentRuleSet:
    """Store an immutable collection of document rules."""

    rules: tuple[DocumentRule, ...] = ()

    def __post_init__(self) -> None:
        """Validate rule identifiers."""

        identifiers = [
            rule.id
            for rule in self.rules
        ]

        if len(identifiers) != len(
            set(identifiers),
        ):
            raise ValueError(
                "Document rule identifiers "
                "must be unique."
            )

    def get(
        self,
        rule_id: str,
    ) -> DocumentRule | None:
        """Return a document rule by identifier."""

        for rule in self.rules:
            if rule.id == rule_id:
                return rule

        return None

    def list(
        self,
    ) -> tuple[DocumentRule, ...]:
        """Return rules in declaration order."""

        return self.rules
