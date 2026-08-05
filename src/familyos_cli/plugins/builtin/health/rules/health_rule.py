"""Health rule model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class HealthRule:
    """Describe a FamilyOS health rule."""

    id: str

    name: str

    version: str

    severity: str

    description: str = ""
