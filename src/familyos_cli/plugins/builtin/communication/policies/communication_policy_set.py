"""Communication policy collection."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.communication.policies.communication_policy import (
    CommunicationPolicy,
)


@dataclass(frozen=True, slots=True)
class CommunicationPolicySet:
    """Collection of communication policies."""

    policies: tuple[
        CommunicationPolicy,
        ...,
    ] = ()

    def __post_init__(self) -> None:
        """Validate uniqueness."""

        ids = [
            policy.id
            for policy in self.policies
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Communication policy identifiers must be unique."
            )

    def list(
        self,
    ) -> tuple[
        CommunicationPolicy,
        ...,
    ]:
        """Return all policies."""

        return self.policies

    def get(
        self,
        policy_id: str,
    ) -> CommunicationPolicy | None:
        """Return one policy."""

        for policy in self.policies:
            if policy.id == policy_id:
                return policy

        return None
