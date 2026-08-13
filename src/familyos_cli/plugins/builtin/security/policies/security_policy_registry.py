"""Security policy registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.policies.security_policy import (
    SecurityPolicy,
)


class SecurityPolicyRegistry:
    """Registry for FamilyOS security policies."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._policies: dict[str, SecurityPolicy] = {}

    def register(
        self,
        policy: SecurityPolicy,
    ) -> None:
        """Register a security policy."""

        if policy.id in self._policies:
            raise ValueError(
                f"Security policy '{policy.id}' already registered.",
            )

        self._policies[
            policy.id
        ] = policy

    def get(
        self,
        policy_id: str,
    ) -> SecurityPolicy | None:
        """Return a policy by identifier."""

        return self._policies.get(
            policy_id,
        )

    def list(
        self,
    ) -> tuple[SecurityPolicy, ...]:
        """Return registered policies."""

        return tuple(
            self._policies.values(),
        )
