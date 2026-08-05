"""Education rule model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class EducationRule:
    """Define an education rule."""

    id: str

    name: str

    level: str

    description: str = ""
