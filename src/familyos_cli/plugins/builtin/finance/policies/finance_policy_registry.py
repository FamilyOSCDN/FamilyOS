"""Finance policy registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.policies.finance_policy import (
    FinancePolicy,
)


class FinancePolicyRegistry:
    """Registry for FamilyOS finance policies."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._policies: dict[str, FinancePolicy] = {}

    def register(
        self,
        policy: FinancePolicy,
    ) -> None:
        """Register a finance policy."""

        self._policies[policy.id] = policy

    def get(
        self,
        policy_id: str,
    ) -> FinancePolicy | None:
        """Return a policy by identifier."""

        return self._policies.get(
            policy_id,
        )

    def list(
        self,
    ) -> tuple[FinancePolicy, ...]:
        """Return registered policies."""

        return tuple(
            self._policies.values(),
        )
