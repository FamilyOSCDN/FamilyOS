"""Health policy model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class HealthPolicy:
    """Describe a FamilyOS health policy."""

    id: str

    name: str

    version: str

    description: str = ""
