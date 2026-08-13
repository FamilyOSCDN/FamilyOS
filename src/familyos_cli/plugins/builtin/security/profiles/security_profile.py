"""Security profile model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityProfile:
    """Describe a FamilyOS security profile."""

    id: str

    name: str

    version: str

    level: str

    description: str = ""

    def __post_init__(
        self,
    ) -> None:
        """Validate security profile invariants."""

        if not self.id.strip():
            raise ValueError(
                "Security profile id cannot be empty.",
            )

        if not self.name.strip():
            raise ValueError(
                "Security profile name cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "Security profile version cannot be empty.",
            )

        if not self.level.strip():
            raise ValueError(
                "Security profile level cannot be empty.",
            )
