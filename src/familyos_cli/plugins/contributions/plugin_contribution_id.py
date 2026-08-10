"""Canonical plugin contribution identifier."""

from __future__ import annotations

import re
from dataclasses import dataclass

_CONTRIBUTION_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+){2,}$",
)


@dataclass(
    frozen=True,
    slots=True,
)
class PluginContributionId:
    """Identify a plugin contribution canonically."""

    value: str

    def __post_init__(
        self,
    ) -> None:
        """Validate the canonical contribution identifier."""

        if not self.value:
            raise ValueError(
                "Plugin contribution id cannot be empty.",
            )

        if not _CONTRIBUTION_ID_PATTERN.fullmatch(
            self.value,
        ):
            raise ValueError(
                (
                    "Invalid plugin contribution id: "
                    f"'{self.value}'."
                ),
            )

    def __str__(
        self,
    ) -> str:
        """Return the canonical identifier value."""

        return self.value
