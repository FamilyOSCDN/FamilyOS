"""Finance policy model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class FinancePolicy:
    """Describe a FamilyOS finance policy."""

    id: str

    name: str

    version: str

    description: str = ""
