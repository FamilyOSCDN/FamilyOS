"""Document policy set."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.documents.policies.document_policy import (
    DocumentPolicy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentPolicySet:
    """Store an immutable collection of document policies."""

    policies: tuple[DocumentPolicy, ...] = ()

    def __post_init__(self) -> None:
        """Validate policy identifiers."""

        identifiers = [
            policy.id
            for policy in self.policies
        ]

        if len(identifiers) != len(
            set(identifiers),
        ):
            raise ValueError(
                "Document policy identifiers "
                "must be unique."
            )

    def get(
        self,
        policy_id: str,
    ) -> DocumentPolicy | None:
        """Return a document policy by identifier."""

        for policy in self.policies:
            if policy.id == policy_id:
                return policy

        return None

    def list(
        self,
    ) -> tuple[DocumentPolicy, ...]:
        """Return policies in declaration order."""

        return self.policies
