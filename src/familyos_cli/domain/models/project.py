"""Project model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    """Describe a FamilyOS project."""

    name: str