"""Security rule model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityRule:
    """Describe a FamilyOS security rule."""

    id: str

    name: str

    version: str

    severity: str

    description: str = ""

    def __post_init__(
        self,
    ) -> None:
        """Validate security rule invariants."""

        if not self.id.strip():
            raise ValueError(
                "Security rule id cannot be empty.",
            )

        if not self.name.strip():
            raise ValueError(
                "Security rule name cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "Security rule version cannot be empty.",
            )

        if not self.severity.strip():
            raise ValueError(
                "Security rule severity cannot be empty.",
            )
