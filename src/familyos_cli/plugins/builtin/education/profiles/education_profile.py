"""Education profile model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class EducationProfile:
    """Define an education profile."""

    id: str

    name: str

    level: str

    description: str = ""
