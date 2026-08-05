"""Education policy model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class EducationPolicy:
    """Define an education policy."""

    id: str

    name: str

    level: str

    description: str = ""
