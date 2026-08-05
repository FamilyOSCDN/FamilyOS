"""Finance profile resolver."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)
from familyos_cli.plugins.builtin.finance.profiles.finance_profile import (
    FinanceProfile,
)


class FinanceProfileResolver:
    """Resolve finance profiles."""

    def resolve(
        self,
        profile: FinanceProfile,
    ) -> FinanceLevel:
        """Resolve profile level."""

        return FinanceLevel(
            profile.level.lower(),
        )
