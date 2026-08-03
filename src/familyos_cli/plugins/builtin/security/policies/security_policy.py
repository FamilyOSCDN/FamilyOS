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