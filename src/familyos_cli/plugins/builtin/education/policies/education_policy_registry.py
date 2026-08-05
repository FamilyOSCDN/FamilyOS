"""Education policy registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.policies.education_policy import (
    EducationPolicy,
)


class EducationPolicyRegistry:
    """Store education policies."""

    def __init__(self) -> None:
        self._policies: dict[str, EducationPolicy] = {}

    def register(
        self,
        policy: EducationPolicy,
    ) -> None:
        """Register a policy."""

        self._policies[policy.id] = policy

    def get(
        self,
        policy_id: str,
    ) -> EducationPolicy | None:
        """Get policy by identifier."""

        return self._policies.get(
            policy_id,
        )

    def list(
        self,
    ) -> tuple[EducationPolicy, ...]:
        """List registered policies."""

        return tuple(
            self._policies.values(),
        )
