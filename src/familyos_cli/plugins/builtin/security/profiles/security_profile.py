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
