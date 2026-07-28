"""Project model."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Project:
    """Represent a FamilyOS project."""

    name: str
