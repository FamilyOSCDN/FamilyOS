"""Security policy model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityPolicy:
    """Describe a FamilyOS security policy."""

    id: str

    name: str

    version: str

    description: str = ""

    def __post_init__(
        self,
    ) -> None:
        """Validate security policy invariants."""

        if not self.id.strip():
            raise ValueError(
                "Security policy id cannot be empty.",
            )

        if not self.name.strip():
            raise ValueError(
                "Security policy name cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "Security policy version cannot be empty.",
            )
