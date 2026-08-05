"""Finance rule model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class FinanceRule:
    """Describe a FamilyOS finance rule."""

    id: str

    name: str

    version: str

    severity: str

    description: str = ""
