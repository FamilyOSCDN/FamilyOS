"""Health policy registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.policies.health_policy import (
    HealthPolicy,
)


class HealthPolicyRegistry:
    """Registry for FamilyOS health policies."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._policies: dict[str, HealthPolicy] = {}

    def register(
        self,
        policy: HealthPolicy,
    ) -> None:
        """Register a health policy."""

        self._policies[policy.id] = policy

    def get(
        self,
        policy_id: str,
    ) -> HealthPolicy | None:
        """Return a policy by identifier."""

        return self._policies.get(
            policy_id,
        )

    def list(
        self,
    ) -> tuple[HealthPolicy, ...]:
        """Return registered policies."""

        return tuple(
            self._policies.values(),
        )
